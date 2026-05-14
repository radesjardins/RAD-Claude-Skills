# Vision

## Product statement

Wayfinder helps outdoor enthusiasts and trip planners pick optimal travel windows by combining real-time weather forecast data with activity-specific constraints (e.g., "I need clear visibility AND wind under 15mph").

## Problem

Current trip-planning alternatives fail because:

- Weather apps surface conditions but don't reason about activity constraints
- Trip-planning sites optimize for booking, not for activity feasibility
- Outdoor enthusiasts end up cross-referencing 3+ tools to make a single go/no-go call

## Target users

- Primary: hobbyist outdoor enthusiasts planning weekend trips
- Secondary: small-group trip leaders who coordinate for 5–10 people
- Not a target user: enterprise logistics, commercial fleet planning, time-critical professional ops

## Product principles

- Trust requires transparency: every recommendation surfaces the reasoning
- Constraints are user-specified, not hardcoded: the tool serves activity-specific needs, not generic averages
- Fast over feature-rich: a usable answer in 5 seconds beats a comprehensive answer in 30

## Non-goals

- Not building native mobile apps for v1 — web-responsive only
- Not optimizing for enterprise multi-tenant use cases
- Not handling time-critical safety operations (search-and-rescue, etc.)
- Not building social features (sharing, comments, leaderboards)

## Success signals

- User outcome: 80% of users complete a go/no-go decision in under 60 seconds
- Product metric: 30% of users return within 7 days of first use
- Engineering outcome: weather provider rate-limit failures don't cascade to user-facing errors
