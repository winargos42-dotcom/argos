from fastapi import APIRouter, HTTPException
from starlette.concurrency import run_in_threadpool

from src.runtime_registry import read_registry, resolve_api, resolve_path
from src.runtime_discovery import refresh, sync_repository


def create_discovery_router():
    router = APIRouter(prefix='/api/discovery')

    @router.get('')
    def status():
        value = read_registry()
        if not value:
            raise HTTPException(503, 'Карта системы ещё не проверена')
        return value

    @router.get('/resolve/{kind}/{name}')
    def resolve(kind: str, name: str, machine_id: str | None = None):
        if kind not in {'path', 'api'}:
            raise HTTPException(422, 'Поддерживаются path и api')
        value = (resolve_path if kind == 'path' else resolve_api)(name, machine_id=machine_id)
        if value is None:
            raise HTTPException(409, 'Ресурс недоступен или проверка устарела')
        return {'kind': kind, 'name': name, 'value': value, 'verified': True}

    @router.post('/refresh')
    async def update():
        try:
            return await run_in_threadpool(refresh)
        except BlockingIOError:
            raise HTTPException(409, 'Обновление карты уже выполняется') from None
        except Exception:
            raise HTTPException(503, 'Карта не обновлена; проверьте локальный журнал discovery') from None

    @router.post('/repositories/{repository_id}/sync')
    async def sync(repository_id: str, apply: bool = False):
        snapshot = read_registry()
        local = snapshot.get('machines', {}).get(snapshot.get('local_id'), {})
        selected = next((r for r in local.get('repositories', []) if r.get('id') == repository_id), None)
        if selected is None:
            raise HTTPException(404, 'Известный локальный репозиторий не найден')
        result = await run_in_threadpool(sync_repository, selected['path'], apply=apply, expected=selected)
        if result['state'] == 'conflict':
            raise HTTPException(409, result['reason'])
        return result

    return router
