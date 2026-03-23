# Schema Types Guide

Complete reference for all Google-supported structured data types. Use JSON-LD format (Google's strong recommendation over Microdata/RDFa).

## Implementation Rules

1. **JSON-LD only** — easier to maintain, less error-prone, supports nesting, injectable via GTM
2. **Match visible content** — never mark up content hidden from users
3. **Use most specific type** — don't label woodworking instructions as Recipe
4. **Completeness over quantity** — fewer but highly complete properties beat many sparse ones
5. **Validate always** — use Google Rich Results Test before deploying

## Schema Types by Category

### Business & Organization
| Type | Use When | Key Properties | Rich Result |
|------|----------|---------------|-------------|
| Organization | Every site (homepage) | name, url, logo, sameAs, contactPoint | Knowledge Panel |
| LocalBusiness | Physical locations | address, geo, openingHours, priceRange | Local Pack |
| ProfilePage | Author/team pages | mainEntity (Person), dateCreated | Enhanced profile |

### Content & Articles
| Type | Use When | Key Properties | Rich Result |
|------|----------|---------------|-------------|
| Article | News/blog posts | headline, author, datePublished, image | Top Stories |
| BlogPosting | Blog content | Same as Article + blog-specific | Article rich result |
| HowTo | Step-by-step guides | step[], totalTime, tool[], supply[] | How-to rich result |
| FAQPage | FAQ sections | mainEntity[Question > acceptedAnswer] | FAQ accordion |
| QAPage | Single Q&A | mainEntity[Question > acceptedAnswer] | Q&A rich result |

### E-Commerce
| Type | Use When | Key Properties | Rich Result |
|------|----------|---------------|-------------|
| Product | Product pages | name, image, offers, review, sku | Product snippet |
| ProductGroup | Variant products | productGroupID, variesBy, hasVariant | Grouped products |
| AggregateOffer | Price ranges | lowPrice, highPrice, offerCount | Price range display |
| MerchantReturnPolicy | Return info | returnPolicyCategory, returnWindow | Return info snippet |
| ShippingService | Shipping details | deliveryTime, shippingRate | Shipping snippet |
| MemberProgram | Loyalty programs | membershipPoints, tiers | Loyalty display |

### Reviews & Ratings
| Type | Use When | Key Properties | Rich Result |
|------|----------|---------------|-------------|
| Review | Individual reviews | reviewRating, author, itemReviewed | Review stars |
| AggregateRating | Rating summaries | ratingValue, reviewCount, bestRating | Star snippet |
| EmployerAggregateRating | Employer reviews | ratingValue, reviewCount | Employer stars |

### Events & Courses
| Type | Use When | Key Properties | Rich Result |
|------|----------|---------------|-------------|
| Event | Events/conferences | startDate, location, offers, performer | Event listing |
| Course | Educational content | name, provider, hasCourseInstance | Course listing |
| CourseInstance | Specific offerings | courseMode, instructor, courseSchedule | Enhanced course |

### Media
| Type | Use When | Key Properties | Rich Result |
|------|----------|---------------|-------------|
| VideoObject | Video content | name, uploadDate, thumbnailUrl, duration | Video carousel |
| Clip | Video segments | name, startOffset, endOffset | Key moments |
| BroadcastEvent | Live streams | isLiveBroadcast, startDate | LIVE badge |
| Movie | Film pages | name, director, dateCreated | Movie panel |
| Book | Book pages | name, author, isbn, workExample | Book panel |
| Recipe | Recipes | recipeIngredient, recipeInstructions, nutrition | Recipe card |

### Navigation & Structure
| Type | Use When | Key Properties | Rich Result |
|------|----------|---------------|-------------|
| BreadcrumbList | All pages | itemListElement[position, name, item] | Breadcrumb trail |
| ItemList | List/carousel pages | itemListElement[], numberOfItems | Carousel |
| WebSite | Homepage | name, url, potentialAction[SearchAction] | Sitelinks searchbox |

### Professional & Jobs
| Type | Use When | Key Properties | Rich Result |
|------|----------|---------------|-------------|
| JobPosting | Job listings | title, datePosted, hiringOrganization, salary | Job listing |
| EducationOccupationalProgram | Degree programs | programType, provider | Program listing |

### Specialized
| Type | Use When | Key Properties | Rich Result |
|------|----------|---------------|-------------|
| SoftwareApplication | Software/app pages | name, operatingSystem, offers, rating | App snippet |
| MathSolver | Math tools | potentialAction[SolveMathAction] | Math solver |
| ClaimReview | Fact checks | claimReviewed, reviewRating | Fact check label |
| Speakable (BETA) | Voice/AI-ready content | cssSelector or xpath | Voice assistant |
| VacationRental | Rental listings | address, geo, numberOfRooms | Rental listing |

## JSON-LD Template

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "TypeName",
  "property1": "value1",
  "property2": {
    "@type": "NestedType",
    "nestedProperty": "value"
  }
}
</script>
```

## Framework Integration

### Next.js (App Router)
Use the `metadata` export or a `<Script>` component with `strategy="beforeInteractive"` to inject JSON-LD into the page head. Serialize the schema object with `JSON.stringify()`.

### React (General)
Create a `<JsonLd>` component that renders a `<script>` tag with `type="application/ld+json"` and the serialized schema data. Use a sanitization library if the data includes user-generated content.

### Static HTML
Place the `<script type="application/ld+json">` block directly in the `<head>` or `<body>` of your HTML.

### Google Tag Manager
Inject JSON-LD via Custom HTML tags — useful for sites where you can't modify source code directly.

## AEO-Critical Schema Types

These schema types are particularly important for AI search visibility:
1. **FAQPage** — LLMs extract Q&A pairs directly
2. **HowTo** — Step-by-step content is highly citable
3. **Organization** — Defines your brand entity for AI
4. **Product** — Enables AI product recommendations
5. **Speakable** — Explicitly marks content for voice/AI reading
6. **Review/AggregateRating** — AI uses ratings for recommendations
