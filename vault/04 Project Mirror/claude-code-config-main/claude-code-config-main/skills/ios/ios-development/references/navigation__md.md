---
argos_import: project_file
source_path: claude-code-config-main/claude-code-config-main/skills/ios/ios-development/references/navigation.md
source_abs: F:\debug\argoss\claude-code-config-main\claude-code-config-main\skills\ios\ios-development\references\navigation.md
source_ext: .md
source_sha256: 6db8c30c79cc35b69bcf7db5db69c41a9ced75140c3e6e568fab1c19af51e352
text_sha256: 6db8c30c79cc35b69bcf7db5db69c41a9ced75140c3e6e568fab1c19af51e352
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:26
---

# navigation.md

- Source: `claude-code-config-main/claude-code-config-main/skills/ios/ios-development/references/navigation.md`
- Extract: `text`
- SHA256: `6db8c30c79cc35b69bcf7db5db69c41a9ced75140c3e6e568fab1c19af51e352`

## Content

# iOS Navigation Reference

## Table of contents
1. NavigationStack (iOS 16+)
2. Tab navigation
3. Sheets & overlays
4. Coordinator pattern
5. Deep links & URL routing
6. UIKit navigation (legacy)

---

## 1. NavigationStack (iOS 16+)

### Type-safe path navigation
```swift
// Define routes
enum Route: Hashable {
    case productList
    case productDetail(Product)
    case cart
    case checkout(Cart)
    case orderConfirmation(Order)
}

// Root view
struct ShopView: View {
    @State private var path = NavigationPath()
    
    var body: some View {
        NavigationStack(path: $path) {
            ProductListView(path: $path)
                .navigationDestination(for: Route.self) { route in
                    switch route {
                    case .productList: ProductListView(path: $path)
                    case .productDetail(let p): ProductDetailView(product: p, path: $path)
                    case .cart: CartView(path: $path)
                    case .checkout(let c): CheckoutView(cart: c, path: $path)
                    case .orderConfirmation(let o): OrderConfirmView(order: o)
                    }
                }
        }
    }
}

// Navigate from child
struct ProductDetailView: View {
    let product: Product
    @Binding var path: NavigationPath
    
    var body: some View {
        Button("Add to Cart") {
            path.append(Route.cart)
        }
    }
}
```

### Programmatic navigation (pop, pop to root)
```swift
path.removeLast()              // pop one
path = NavigationPath()        // pop to root
path.append(Route.cart)        // push
```

---

## 2. Tab navigation

```swift
struct MainTabView: View {
    @State private var selectedTab: Tab = .home
    
    enum Tab: Hashable {
        case home, search, favorites, profile
    }
    
    var body: some View {
        TabView(selection: $selectedTab) {
            HomeTab()
                .tabItem { Label("Home", systemImage: "house") }
                .tag(Tab.home)
            
            SearchTab()
                .tabItem { Label("Search", systemImage: "magnifyingglass") }
                .tag(Tab.search)
            
            FavoritesTab()
                .tabItem { Label("Saved", systemImage: "heart") }
                .badge(favoritesCount)
                .tag(Tab.favorites)
            
            ProfileTab()
                .tabItem { Label("Profile", systemImage: "person") }
                .tag(Tab.profile)
        }
    }
}
```

**Each tab should have its own NavigationStack** to maintain independent navigation state:
```swift
func HomeTab() -> some View {
    NavigationStack {
        HomeView()
    }
}
```

---

## 3. Sheets & overlays

```swift
// Sheet
@State private var showingSettings = false

.sheet(isPresented: $showingSettings) {
    SettingsView()
        .presentationDetents([.medium, .large])
        .presentationDragIndicator(.visible)
}

// Full screen
@State private var showingOnboarding = false
.fullScreenCover(isPresented: $showingOnboarding) {
    OnboardingView()
}

// Item-based (auto-dismiss when nil)
@State private var selectedProduct: Product?
.sheet(item: $selectedProduct) { product in
    ProductDetailSheet(product: product)
}

// Alert with actions
@State private var showDeleteAlert = false
.alert("Delete Product?", isPresented: $showDeleteAlert) {
    Button("Delete", role: .destructive) { deleteProduct() }
    Button("Cancel", role: .cancel) { }
} message: {
    Text("This action cannot be undone.")
}

// Confirmation dialog (action sheet)
.confirmationDialog("Options", isPresented: $showOptions, titleVisibility: .visible) {
    Button("Share") { share() }
    Button("Delete", role: .destructive) { delete() }
    Button("Cancel", role: .cancel) { }
}
```

---

## 4. Coordinator pattern

Keeps navigation logic out of Views and ViewModels.

```swift
// Protocol
protocol CoordinatorProtocol: AnyObject {
    func navigate(to route: AppRoute)
    func present(_ route: AppRoute)
    func dismiss()
    func pop()
    func popToRoot()
}

// Implementation
@Observable
final class AppCoordinator: CoordinatorProtocol {
    var navigationPath = NavigationPath()
    var presentedSheet: AppRoute?
    var presentedFullScreen: AppRoute?
    
    func navigate(to route: AppRoute) {
        navigationPath.append(route)
    }
    
    func present(_ route: AppRoute) {
        presentedSheet = route
    }
    
    func dismiss() {
        presentedSheet = nil
        presentedFullScreen = nil
    }
    
    func pop() { navigationPath.removeLast() }
    func popToRoot() { navigationPath = NavigationPath() }
}

// Root wiring
struct RootView: View {
    @State private var coordinator = AppCoordinator()
    
    var body: some View {
        NavigationStack(path: $coordinator.navigationPath) {
            HomeView()
                .environment(coordinator)
                .navigationDestination(for: AppRoute.self) { route in
                    routeView(route)
                }
        }
        .sheet(item: $coordinator.presentedSheet) { route in
            routeView(route)
                .environment(coordinator)
        }
    }
    
    @ViewBuilder
    func routeView(_ route: AppRoute) -> some View {
        switch route {
        case .home: HomeView()
        case .profile(let id): ProfileView(userId: id)
        case .settings: SettingsView()
        }
    }
}

// Child view — only knows about coordinator
struct HomeView: View {
    @Environment(AppCoordinator.self) private var coordinator
    
    var body: some View {
        Button("Profile") {
            coordinator.navigate(to: .profile(currentUserId))
        }
    }
}
```

---

## 5. Deep links & URL routing

```swift
// App entry
@main
struct MyApp: App {
    @State private var coordinator = AppCoordinator()
    
    var body: some Scene {
        WindowGroup {
            RootView()
                .environment(coordinator)
                .onOpenURL { url in
                    handleDeepLink(url)
                }
        }
    }
    
    private func handleDeepLink(_ url: URL) {
        // myapp://product/123
        // https://myapp.com/product/123
        guard let route = DeepLinkRouter.route(from: url) else { return }
        coordinator.navigate(to: route)
    }
}

// Router
enum DeepLinkRouter {
    static func route(from url: URL) -> AppRoute? {
        guard url.host == "product",
              let id = url.pathComponents.dropFirst().first else { return nil }
        return .productDetail(id: id)
    }
}
```

### Universal links setup
1. Add `Associated Domains` capability in Xcode: `applinks:yourdomain.com`
2. Host `apple-app-site-association` at `https://yourdomain.com/.well-known/apple-app-site-association`:
```json
{
  "applinks": {
    "details": [
      {
        "appIDs": ["TEAMID.com.yourapp"],
        "components": [
          { "/": "/product/*" },
          { "/": "/profile/*" }
        ]
      }
    ]
  }
}
```

---

## 6. UIKit navigation (when needed)

```swift
// Push
navigationController?.pushViewController(ProductDetailVC(product: product), animated: true)

// Present
let vc = SettingsVC()
let nav = UINavigationController(rootViewController: vc)
nav.modalPresentationStyle = .formSheet
present(nav, animated: true)

// Pop
navigationController?.popViewController(animated: true)
navigationController?.popToRootViewController(animated: true)

// Dismiss
dismiss(animated: true)
```

### UIKit + SwiftUI bridge
```swift
// Use SwiftUI view inside UIKit
let hostingVC = UIHostingController(rootView: ProductListView())
navigationController?.pushViewController(hostingVC, animated: true)

// Use UIKit view controller in SwiftUI
struct LegacyMapView: UIViewControllerRepresentable {
    func makeUIViewController(context: Context) -> MKMapViewController {
        MKMapViewController()
    }
    func updateUIViewController(_ vc: MKMapViewController, context: Context) { }
}
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
