# Content Collections Patterns

## Basic Blog Collection

```ts
// src/content.config.ts
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: ({ image }) => z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    heroImage: image().optional(),
    author: z.string().default('Anonymous'),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
```

## Multi-Collection with References

```ts
const authors = defineCollection({
  loader: glob({ pattern: '**/*.json', base: './src/content/authors' }),
  schema: z.object({
    name: z.string(),
    bio: z.string(),
    avatar: z.string().url(),
  }),
});

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    author: z.reference('authors'),
    relatedPosts: z.array(z.reference('blog')).optional(),
  }),
});

export const collections = { authors, blog };
```

## Remote API Loader

```ts
const products = defineCollection({
  loader: async () => {
    const res = await fetch('https://api.example.com/products');
    const data = await res.json();
    return data.map((item: any) => ({
      id: item.slug,
      ...item,
    }));
  },
  schema: z.object({
    name: z.string(),
    price: z.number(),
    inStock: z.boolean(),
  }),
});
```

## Querying Patterns

```astro
---
// List page: get all, filter, sort
import { getCollection } from 'astro:content';

const posts = await getCollection('blog', ({ data }) => !data.draft);
const sorted = posts.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
---

---
// Detail page: get single entry
import { getEntry } from 'astro:content';

import { render } from 'astro:content';

const post = await getEntry('blog', Astro.params.id);
if (!post) return Astro.redirect('/404');
const { Content } = await render(post);
---
<Content />
```

## Key Rules

- `z.coerce.date()` over `z.date()` — always
- `image()` helper for local image validation
- `.optional()` and `.default()` liberally — don't over-require
- `z.reference()` for cross-collection relationships
- Content Layer rebuilds at build time only — no runtime updates without a new build
