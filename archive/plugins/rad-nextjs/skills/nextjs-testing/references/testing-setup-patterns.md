# Next.js Testing Setup Patterns

Complete configuration templates for Vitest, Cypress, and Playwright with Next.js.

---

## Vitest Setup (Unit & Component Testing)

### Installation

```bash
npm install -D vitest @vitejs/plugin-react @testing-library/react @testing-library/jest-dom jsdom
```

### Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./vitest.setup.ts'],
    include: ['**/*.test.{ts,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', '.next/', '**/*.config.*'],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './'),
    },
  },
});
```

```typescript
// vitest.setup.ts
import '@testing-library/jest-dom/vitest';
```

### Example Unit Test

```typescript
// lib/__tests__/utils.test.ts
import { describe, it, expect } from 'vitest';
import { formatPrice, validateEmail } from '../utils';

describe('formatPrice', () => {
  it('formats cents to dollars', () => {
    expect(formatPrice(1999)).toBe('$19.99');
  });

  it('handles zero', () => {
    expect(formatPrice(0)).toBe('$0.00');
  });
});
```

### Example Component Test

```tsx
// components/__tests__/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { Button } from '../Button';

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: 'Click me' })).toBeInTheDocument();
  });

  it('calls onClick handler', () => {
    const onClick = vi.fn();
    render(<Button onClick={onClick}>Click</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(onClick).toHaveBeenCalledOnce();
  });

  it('disables when loading', () => {
    render(<Button loading>Submit</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

### Package.json Scripts

```json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage"
  }
}
```

---

## Cypress Setup (E2E Testing)

### Installation

```bash
npm install -D cypress start-server-and-test
```

### Configuration

```typescript
// cypress.config.ts
import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: false,               // Enable in CI for debugging
    screenshotOnRunFailure: true,
    defaultCommandTimeout: 10000,
    setupNodeEvents(on, config) {
      // Register plugins here
    },
  },
});
```

### Package.json Scripts

```json
{
  "scripts": {
    "build": "next build",
    "start": "next start",
    "cypress:open": "cypress open",
    "cypress:run": "cypress run",
    "test:e2e": "start-server-and-test start http://localhost:3000 cypress:run"
  }
}
```

### Custom Commands

```typescript
// cypress/support/commands.ts

// Programmatic login with session caching
Cypress.Commands.add('login', (email = 'test@example.com', password = 'password123') => {
  cy.session([email, password], () => {
    cy.request({
      method: 'POST',
      url: '/api/auth/login',
      body: { email, password },
    }).then((response) => {
      expect(response.status).to.eq(200);
    });
  });
});

// Assert no console errors on page
Cypress.Commands.add('assertNoConsoleErrors', () => {
  cy.window().then((win) => {
    cy.spy(win.console, 'error').as('consoleError');
  });
  // At end of test: cy.get('@consoleError').should('not.have.been.called');
});
```

```typescript
// cypress/support/e2e.ts
import './commands';
```

### Example E2E Test

```typescript
// cypress/e2e/products.cy.ts
describe('Product Catalog', () => {
  beforeEach(() => {
    // Clean state BEFORE test (not after)
    cy.request('POST', '/api/test/reset-db');
    cy.login();
  });

  it('displays product list from server component', () => {
    cy.visit('/products');

    // Wait for server-rendered content (no arbitrary waits)
    cy.get('[data-testid="product-grid"]').should('be.visible');
    cy.get('[data-testid="product-card"]').should('have.length.at.least', 1);
  });

  it('adds product to cart via server action', () => {
    cy.visit('/products');
    cy.get('[data-testid="product-card"]').first().click();
    cy.get('[data-testid="add-to-cart"]').click();

    // Verify server action completed
    cy.get('[data-testid="cart-count"]').should('contain', '1');
  });

  it('handles streaming content with suspense', () => {
    cy.visit('/dashboard');

    // Skeleton appears first
    cy.get('[data-testid="stats-skeleton"]').should('be.visible');

    // Real content streams in
    cy.get('[data-testid="stats-loaded"]').should('be.visible');
    cy.get('[data-testid="stats-skeleton"]').should('not.exist');
  });
});
```

### API Route Testing

```typescript
// cypress/e2e/api.cy.ts
describe('API Routes', () => {
  it('returns products with correct schema', () => {
    cy.request('GET', '/api/products').then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.be.an('array');
      expect(response.body[0]).to.have.keys(['id', 'name', 'price']);
    });
  });

  it('rejects unauthenticated requests', () => {
    cy.request({
      method: 'POST',
      url: '/api/admin/users',
      failOnStatusCode: false,
    }).then((response) => {
      expect(response.status).to.eq(401);
    });
  });

  it('validates input schema', () => {
    cy.login();
    cy.request({
      method: 'POST',
      url: '/api/products',
      body: { name: '', price: -1 },  // Invalid
      failOnStatusCode: false,
    }).then((response) => {
      expect(response.status).to.eq(400);
    });
  });
});
```

### Network Interception (Mocking)

```typescript
// Mock API responses for UI testing
it('shows empty state when no products', () => {
  cy.intercept('GET', '/api/products', { body: [] }).as('getProducts');
  cy.visit('/products');
  cy.wait('@getProducts');
  cy.get('[data-testid="empty-state"]').should('be.visible');
});

it('handles server error gracefully', () => {
  cy.intercept('GET', '/api/products', { statusCode: 500 }).as('getProducts');
  cy.visit('/products');
  cy.wait('@getProducts');
  cy.get('[data-testid="error-message"]').should('be.visible');
});
```

---

## Playwright Setup (E2E Testing)

### Installation

```bash
npm install -D @playwright/test
npx playwright install
```

### Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    // Mobile viewports
    { name: 'mobile-chrome', use: { ...devices['Pixel 5'] } },
    { name: 'mobile-safari', use: { ...devices['iPhone 12'] } },
  ],
  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
});
```

### Auth Setup (Reusable State)

```typescript
// tests/auth.setup.ts
import { test as setup, expect } from '@playwright/test';

const authFile = 'tests/.auth/user.json';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('test@example.com');
  await page.getByLabel('Password').fill('password123');
  await page.getByRole('button', { name: 'Sign in' }).click();
  await page.waitForURL('/dashboard');
  await page.context().storageState({ path: authFile });
});
```

```typescript
// playwright.config.ts — add auth project
projects: [
  { name: 'setup', testMatch: /.*\.setup\.ts/ },
  {
    name: 'chromium',
    use: {
      ...devices['Desktop Chrome'],
      storageState: 'tests/.auth/user.json',
    },
    dependencies: ['setup'],
  },
],
```

### Example E2E Test

```typescript
// tests/products.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Product Catalog', () => {
  test('displays server-rendered product list', async ({ page }) => {
    await page.goto('/products');

    // Wait for content
    const grid = page.getByTestId('product-grid');
    await expect(grid).toBeVisible();

    const cards = page.getByTestId('product-card');
    expect(await cards.count()).toBeGreaterThan(0);
  });

  test('search filters products', async ({ page }) => {
    await page.goto('/products');

    await page.getByTestId('search-input').fill('laptop');
    await page.getByTestId('search-button').click();

    // Wait for filtered results
    await expect(page.getByTestId('product-card')).toHaveCount(3);
  });

  test('handles streaming suspense content', async ({ page }) => {
    await page.goto('/dashboard');

    // Skeleton appears first
    await expect(page.getByTestId('stats-skeleton')).toBeVisible();

    // Content streams in (auto-waits with retry)
    await expect(page.getByTestId('stats-loaded')).toBeVisible({ timeout: 10000 });
  });
});
```

### API Testing with Playwright

```typescript
// tests/api.spec.ts
import { test, expect } from '@playwright/test';

test.describe('API Routes', () => {
  test('GET /api/products returns valid data', async ({ request }) => {
    const response = await request.get('/api/products');
    expect(response.ok()).toBeTruthy();

    const products = await response.json();
    expect(products).toBeInstanceOf(Array);
    expect(products[0]).toHaveProperty('id');
    expect(products[0]).toHaveProperty('name');
  });

  test('POST /api/products validates input', async ({ request }) => {
    const response = await request.post('/api/products', {
      data: { name: '', price: -1 },
    });
    expect(response.status()).toBe(400);
  });
});
```

### Route Mocking

```typescript
test('shows error state on API failure', async ({ page }) => {
  await page.route('/api/products', (route) => {
    route.fulfill({ status: 500, body: 'Internal Server Error' });
  });

  await page.goto('/products');
  await expect(page.getByTestId('error-message')).toBeVisible();
});
```

---

## Test Organization Best Practices

```
project/
├── __tests__/           # Vitest unit tests (colocated or centralized)
│   ├── lib/
│   │   └── utils.test.ts
│   └── components/
│       └── Button.test.tsx
├── cypress/
│   ├── e2e/             # Cypress E2E tests
│   │   ├── auth.cy.ts
│   │   ├── products.cy.ts
│   │   └── api.cy.ts
│   ├── support/
│   │   ├── commands.ts
│   │   └── e2e.ts
│   └── fixtures/        # Test data
├── tests/               # Playwright E2E tests
│   ├── auth.setup.ts
│   ├── products.spec.ts
│   └── .auth/           # Persisted auth state (gitignored)
├── vitest.config.ts
├── cypress.config.ts
└── playwright.config.ts
```

**Choose one E2E framework** (Cypress OR Playwright), not both. Use Vitest for unit/component tests alongside your chosen E2E tool.
