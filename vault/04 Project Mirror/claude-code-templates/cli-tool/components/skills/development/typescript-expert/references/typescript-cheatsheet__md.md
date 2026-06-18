---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/typescript-expert/references/typescript-cheatsheet.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\typescript-expert\references\typescript-cheatsheet.md
source_ext: .md
source_sha256: d3d5ba4fa2da3b06e3703e66b1bbd0d692653cc8bbcd7b364d06d9298cc2a829
text_sha256: 48e2298805f0f0f1081a2a3637470dac17714f838b6ae594a036a1c5364b6c5a
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:46
---

# typescript-cheatsheet.md

- Source: `claude-code-templates/cli-tool/components/skills/development/typescript-expert/references/typescript-cheatsheet.md`
- Extract: `text`
- SHA256: `d3d5ba4fa2da3b06e3703e66b1bbd0d692653cc8bbcd7b364d06d9298cc2a829`

## Content

# TypeScript Cheatsheet

## Type Basics

```typescript
// Primitives
const name: string = 'John'
const age: number = 30
const isActive: boolean = true
const nothing: null = null
const notDefined: undefined = undefined

// Arrays
const numbers: number[] = [1, 2, 3]
const strings: Array<string> = ['a', 'b', 'c']

// Tuple
const tuple: [string, number] = ['hello', 42]

// Object
const user: { name: string; age: number } = { name: 'John', age: 30 }

// Union
const value: string | number = 'hello'

// Literal
const direction: 'up' | 'down' | 'left' | 'right' = 'up'

// Any vs Unknown
const anyValue: any = 'anything'     // ❌ Avoid
const unknownValue: unknown = 'safe' // ✅ Prefer, requires narrowing
```

## Type Aliases & Interfaces

```typescript
// Type Alias
type Point = {
  x: number
  y: number
}

// Interface (preferred for objects)
interface User {
  id: string
  name: string
  email?: string  // Optional
  readonly createdAt: Date  // Readonly
}

// Extending
interface Admin extends User {
  permissions: string[]
}

// Intersection
type AdminUser = User & { permissions: string[] }
```

## Generics

```typescript
// Generic function
function identity<T>(value: T): T {
  return value
}

// Generic with constraint
function getLength<T extends { length: number }>(item: T): number {
  return item.length
}

// Generic interface
interface ApiResponse<T> {
  data: T
  status: number
  message: string
}

// Generic with default
type Container<T = string> = {
  value: T
}

// Multiple generics
function merge<T, U>(obj1: T, obj2: U): T & U {
  return { ...obj1, ...obj2 }
}
```

## Utility Types

```typescript
interface User {
  id: string
  name: string
  email: string
  age: number
}

// Partial - all optional
type PartialUser = Partial<User>

// Required - all required
type RequiredUser = Required<User>

// Readonly - all readonly
type ReadonlyUser = Readonly<User>

// Pick - select properties
type UserName = Pick<User, 'id' | 'name'>

// Omit - exclude properties
type UserWithoutEmail = Omit<User, 'email'>

// Record - key-value map
type UserMap = Record<string, User>

// Extract - extract from union
type StringOrNumber = string | number | boolean
type OnlyStrings = Extract<StringOrNumber, string>

// Exclude - exclude from union
type NotString = Exclude<StringOrNumber, string>

// NonNullable - remove null/undefined
type MaybeString = string | null | undefined
type DefinitelyString = NonNullable<MaybeString>

// ReturnType - get function return type
function getUser() { return { name: 'John' } }
type UserReturn = ReturnType<typeof getUser>

// Parameters - get function parameters
type GetUserParams = Parameters<typeof getUser>

// Awaited - unwrap Promise
type ResolvedUser = Awaited<Promise<User>>
```

## Conditional Types

```typescript
// Basic conditional
type IsString<T> = T extends string ? true : false

// Infer keyword
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T

// Distributive conditional
type ToArray<T> = T extends any ? T[] : never
type Result = ToArray<string | number>  // string[] | number[]

// NonDistributive
type ToArrayNonDist<T> = [T] extends [any] ? T[] : never
```

## Template Literal Types

```typescript
type Color = 'red' | 'green' | 'blue'
type Size = 'small' | 'medium' | 'large'

// Combine
type ColorSize = `${Color}-${Size}`
// 'red-small' | 'red-medium' | 'red-large' | ...

// Event handlers
type EventName = 'click' | 'focus' | 'blur'
type EventHandler = `on${Capitalize<EventName>}`
// 'onClick' | 'onFocus' | 'onBlur'
```

## Mapped Types

```typescript
// Basic mapped type
type Optional<T> = {
  [K in keyof T]?: T[K]
}

// With key remapping
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K]
}

// Filter keys
type OnlyStrings<T> = {
  [K in keyof T as T[K] extends string ? K : never]: T[K]
}
```

## Type Guards

```typescript
// typeof guard
function process(value: string | number) {
  if (typeof value === 'string') {
    return value.toUpperCase()  // string
  }
  return value.toFixed(2)  // number
}

// instanceof guard
class Dog { bark() {} }
class Cat { meow() {} }

function makeSound(animal: Dog | Cat) {
  if (animal instanceof Dog) {
    animal.bark()
  } else {
    animal.meow()
  }
}

// in guard
interface Bird { fly(): void }
interface Fish { swim(): void }

function move(animal: Bird | Fish) {
  if ('fly' in animal) {
    animal.fly()
  } else {
    animal.swim()
  }
}

// Custom type guard
function isString(value: unknown): value is string {
  return typeof value === 'string'
}

// Assertion function
function assertIsString(value: unknown): asserts value is string {
  if (typeof value !== 'string') {
    throw new Error('Not a string')
  }
}
```

## Discriminated Unions

```typescript
// With type discriminant
type Success<T> = { type: 'success'; data: T }
type Error = { type: 'error'; message: string }
type Loading = { type: 'loading' }

type State<T> = Success<T> | Error | Loading

function handle<T>(state: State<T>) {
  switch (state.type) {
    case 'success':
      return state.data  // T
    case 'error':
      return state.message  // string
    case 'loading':
      return null
  }
}

// Exhaustive check
function assertNever(value: never): never {
  throw new Error(`Unexpected value: ${value}`)
}
```

## Branded Types

```typescript
// Create branded type
type Brand<K, T> = K & { __brand: T }

type UserId = Brand<string, 'UserId'>
type OrderId = Brand<string, 'OrderId'>

// Constructor functions
function createUserId(id: string): UserId {
  return id as UserId
}

function createOrderId(id: string): OrderId {
  return id as OrderId
}

// Usage - prevents mixing
function getOrder(orderId: OrderId, userId: UserId) {}

const userId = createUserId('user-123')
const orderId = createOrderId('order-456')

getOrder(orderId, userId)  // ✅ OK
// getOrder(userId, orderId)  // ❌ Error - types don't match
```

## Module Declarations

```typescript
// Declare module for untyped package
declare module 'untyped-package' {
  export function doSomething(): void
  export const value: string
}

// Augment existing module
declare module 'express' {
  interface Request {
    user?: { id: string }
  }
}

// Declare global
declare global {
  interface Window {
    myGlobal: string
  }
}
```

## TSConfig Essentials

```json
{
  "compilerOptions": {
    // Strictness
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    
    // Modules
    "module": "ESNext",
    "moduleResolution": "bundler",
    "esModuleInterop": true,
    
    // Output
    "target": "ES2022",
    "lib": ["ES2022", "DOM"],
    
    // Performance
    "skipLibCheck": true,
    "incremental": true,
    
    // Paths
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

## Best Practices

```typescript
// ✅ Prefer interface for objects
interface User {
  name: string
}

// ✅ Use const assertions
const routes = ['home', 'about'] as const

// ✅ Use satisfies for validation
const config = {
  api: 'https://api.example.com'
} satisfies Record<string, string>

// ✅ Use unknown over any
function parse(input: unknown) {
  if (typeof input === 'string') {
    return JSON.parse(input)
  }
}

// ✅ Explicit return types for public APIs
export function getUser(id: string): User | null {
  // ...
}

// ❌ Avoid
const data: any = fetchData()
data.anything.goes.wrong  // No type safety
```

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Project Mirror Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Project Mirror Hub]]
