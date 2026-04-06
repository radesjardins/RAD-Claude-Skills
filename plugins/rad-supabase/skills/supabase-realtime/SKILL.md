---
name: supabase-realtime
description: >
  This skill should be used when working with Supabase Realtime, setting up database change
  listeners, implementing presence, using broadcast channels, or building real-time features.
  Trigger when: "Supabase Realtime", "realtime subscription", "listen for changes",
  "database changes", "broadcast", "presence", "WebSocket", "channel",
  "real-time updates", "subscribe to table", "Postgres changes",
  "supabase.channel", "realtime configuration",
  or implementing any live/real-time functionality with Supabase.
---

# Supabase Realtime

Guidance for implementing real-time features using Supabase's Realtime service: database change listeners, broadcast messaging, and presence tracking.

## Overview

Supabase Realtime provides three capabilities over WebSocket connections:

| Feature | Description | Use Case |
|---------|-------------|----------|
| **Postgres Changes** | Listen to INSERT, UPDATE, DELETE on tables | Live feeds, notifications |
| **Broadcast** | Send ephemeral messages to channel subscribers | Chat, cursors, typing indicators |
| **Presence** | Track and sync shared state across clients | Online users, collaborative editing |

## Postgres Changes (Database Listeners)

### Subscribe to All Changes on a Table

```typescript
const channel = supabase
  .channel("table-changes")
  .on(
    "postgres_changes",
    { event: "*", schema: "public", table: "messages" },
    (payload) => {
      console.log("Change received:", payload);
    }
  )
  .subscribe();
```

### Subscribe to Specific Events

```typescript
// Only INSERT events
supabase
  .channel("new-messages")
  .on(
    "postgres_changes",
    { event: "INSERT", schema: "public", table: "messages" },
    (payload) => {
      console.log("New message:", payload.new);
    }
  )
  .subscribe();

// Only UPDATE events
supabase
  .channel("message-updates")
  .on(
    "postgres_changes",
    { event: "UPDATE", schema: "public", table: "messages" },
    (payload) => {
      console.log("Updated:", payload.old, "→", payload.new);
    }
  )
  .subscribe();

// Only DELETE events
supabase
  .channel("message-deletes")
  .on(
    "postgres_changes",
    { event: "DELETE", schema: "public", table: "messages" },
    (payload) => {
      console.log("Deleted:", payload.old);
    }
  )
  .subscribe();
```

### Filter by Column Value

```typescript
supabase
  .channel("my-messages")
  .on(
    "postgres_changes",
    {
      event: "INSERT",
      schema: "public",
      table: "messages",
      filter: "room_id=eq.room-123",
    },
    (payload) => {
      console.log("New message in room:", payload.new);
    }
  )
  .subscribe();
```

### Available Filter Operators

| Filter | Example | Description |
|--------|---------|-------------|
| `eq` | `column=eq.value` | Equals |
| `neq` | `column=neq.value` | Not equals |
| `lt`, `gt` | `column=gt.5` | Less/greater than |
| `lte`, `gte` | `column=gte.10` | Less/greater or equal |
| `in` | `column=in.(a,b,c)` | In list |

## Broadcast

Send and receive ephemeral messages without database persistence.

### Send a Broadcast Message

```typescript
const channel = supabase.channel("room-1");

channel.subscribe((status) => {
  if (status === "SUBSCRIBED") {
    channel.send({
      type: "broadcast",
      event: "cursor-move",
      payload: { x: 100, y: 200, userId: "user-123" },
    });
  }
});
```

### Receive Broadcast Messages

```typescript
supabase
  .channel("room-1")
  .on("broadcast", { event: "cursor-move" }, (payload) => {
    console.log("Cursor moved:", payload.payload);
  })
  .subscribe();
```

## Presence

Track which users are online and sync shared state.

### Track User Presence

```typescript
const channel = supabase.channel("online-users");

channel
  .on("presence", { event: "sync" }, () => {
    const state = channel.presenceState();
    console.log("Online users:", state);
  })
  .on("presence", { event: "join" }, ({ key, newPresences }) => {
    console.log("User joined:", key, newPresences);
  })
  .on("presence", { event: "leave" }, ({ key, leftPresences }) => {
    console.log("User left:", key, leftPresences);
  })
  .subscribe(async (status) => {
    if (status === "SUBSCRIBED") {
      await channel.track({
        user_id: "user-123",
        online_at: new Date().toISOString(),
      });
    }
  });
```

### Untrack Presence

```typescript
await channel.untrack();
```

## Unsubscribing

### Remove a Single Channel

```typescript
supabase.removeChannel(channel);
```

### Remove All Channels

```typescript
supabase.removeAllChannels();
```

## Database Configuration for Realtime

### Enable Realtime on a Table

By default, tables are not enabled for Realtime Postgres Changes. Enable via SQL:

```sql
alter publication supabase_realtime add table public.messages;
```

**Via migration (MCP):**
```
mcp__supabase__apply_migration(
  project_id: "<id>",
  name: "enable_realtime_messages",
  query: "alter publication supabase_realtime add table public.messages;"
)
```

### Replica Identity

For UPDATE and DELETE events to include full row data (not just primary key), set `REPLICA IDENTITY FULL`:

```sql
alter table public.messages replica identity full;
```

Without this, `payload.old` in UPDATE/DELETE events only contains the primary key columns.

### Disable Realtime on a Table

```sql
alter publication supabase_realtime drop table public.messages;
```

## RLS and Realtime

Realtime respects RLS policies. Users only receive change events for rows they have SELECT access to. Ensure RLS policies are in place before enabling Realtime — otherwise users may not receive expected events.

**Common issue:** Realtime subscription returns no events, even though data is changing. Check:
1. Table is in the `supabase_realtime` publication
2. RLS policies allow SELECT for the subscribing user
3. Replica identity is set correctly for the event type

## Realtime Logs (MCP)

```
mcp__supabase__get_logs(project_id: "<id>", service: "realtime")
```

Returns WebSocket connection and subscription logs from the last 24 hours.

## Configuration (config.toml)

```toml
[realtime]
enabled = true
# ip_version = "IPv4"  # or IPv6
```

## Common Patterns

### Chat Room

```typescript
// Subscribe to new messages in a room
const channel = supabase
  .channel(`room:${roomId}`)
  .on(
    "postgres_changes",
    {
      event: "INSERT",
      schema: "public",
      table: "messages",
      filter: `room_id=eq.${roomId}`,
    },
    (payload) => addMessage(payload.new)
  )
  .on("presence", { event: "sync" }, () => {
    updateOnlineUsers(channel.presenceState());
  })
  .on("broadcast", { event: "typing" }, ({ payload }) => {
    showTypingIndicator(payload.userId);
  })
  .subscribe();
```

### Live Dashboard

```typescript
// Subscribe to multiple tables
supabase
  .channel("dashboard")
  .on("postgres_changes", { event: "*", schema: "public", table: "orders" }, handleOrderChange)
  .on("postgres_changes", { event: "*", schema: "public", table: "inventory" }, handleInventoryChange)
  .subscribe();
```

## Best Practices

1. **Enable Realtime only on tables that need it** — each table in the publication adds overhead
2. **Set REPLICA IDENTITY FULL** on tables where old values are needed
3. **Use filters** to reduce the volume of events received
4. **Clean up subscriptions** when components unmount or users navigate away
5. **Handle reconnection** — Supabase client auto-reconnects, but refresh state on reconnect
6. **RLS is required** — Realtime enforces RLS, so ensure policies are correct
