---
name: vue-best-practices
description: MUST be used for Vue.js tasks. Strongly recommends Composition API with `<script setup>` and TypeScript as the standard approach. Covers Vue 3, SSR, Volar, vue-tsc. Load for any Vue, .vue files, Vue Router, Pinia, or Vite with Vue work. ALWAYS use Composition API unless the project explicitly requires Options API.
license: MIT
metadata:
  author: github.com/vuejs-ai (adapted for heritage-game)
  version: "18.0.0"
---

# Vue Best Practices Workflow

Use this skill as an instruction set. Follow the workflow in order.

## Core Principles
- **Keep state predictable:** one source of truth, derive everything else.
- **Make data flow explicit:** Props down, Events up for most cases.
- **Favor small, focused components:** easier to test, reuse, and maintain.
- **Avoid unnecessary re-renders:** use computed properties and watchers wisely.
- **Readability counts:** write clear, self-documenting code.

## Project Stack (Heritage Game)
- Vue 3 + Composition API + `<script setup lang="ts">`
- TypeScript strict mode — no `any`
- Tailwind CSS utility-first — no custom CSS except keyframe animations
- Pinia for state management
- Vue Router 4 with `createWebHashHistory()`
- Vite 5 as build tool

## 1) Confirm architecture before coding (required)

- Default stack: Vue 3 + Composition API + `<script setup lang="ts">`
- All components follow the convention in `AGENTS.md` section 10

### 1.1 Component layout order (required)
```vue
<script setup lang="ts">
// 1. imports
// 2. props / emits
// 3. stores
// 4. refs & reactive state
// 5. computed
// 6. lifecycle hooks
// 7. methods / handlers
</script>

<template>
  <!-- Single root element — required for Vue <Transition> -->
</template>

<!-- <style scoped> ONLY for transitions Vue can't handle with Tailwind -->
```

### 1.2 Plan component boundaries before coding (required)

- Define each component's single responsibility in one sentence.
- Route-level views (`*View.vue`) are composition surfaces only — keep them thin.
- Move feature UI into child components under `src/components/`.
- Move stateful logic into composables (`src/composables/use*.ts`).

## 2) Apply essential Vue foundations

### Reactivity
- Keep source state minimal (`ref` / `shallowRef`), derive everything with `computed`.
- Use `shallowRef` for primitive values; use `ref` for objects that need deep reactivity.
- Use watchers only for side effects.
- Avoid recomputing expensive logic inside `<template>`.

### SFC structure and template safety
- Keep SFC sections in order: `<script>` → `<template>` → `<style scoped>`.
- Split large components — if it has 3+ distinct UI sections, it's time to split.
- Keep templates declarative; move branching/logic to `<script setup>`.
- Never use `v-if` + `v-for` on the same element.

### Component data flow
- Props down, events up as primary model.
- Use `v-model` only for true two-way contracts (`defineModel`).
- Use `provide/inject` only for deep-tree dependencies.
- Keep contracts explicit: `defineProps<{...}>()`, `defineEmits<{...}>()`.

### Composables
- Extract logic into composables when reused, stateful, or side-effect heavy.
- Composable file name: `use<Feature>.ts` (e.g. `useSwipe.ts`, `useHaptic.ts`).
- Keep APIs small, typed, and predictable.
- Always null-check browser APIs (Vibration, Web Share, etc.).

## 3) Animations in this project

- All `@keyframes` defined in `tailwind.config.js → theme.extend.keyframes`.
- Respect `prefers-reduced-motion` — fallback to `opacity` fade only.
- Apply `will-change: transform` before complex animation; remove after completion.
- Never use `transition-all` — always specify explicit properties.
- Zone 2 animations should be 20–30% slower than Zone 1 (mystery/tension).

## 4) Performance (post-functionality pass)
- Images: `loading="lazy"` for off-screen assets.
- Prefetch next slide's image while user reads current slide.
- Fallback: gradient background if image hasn't loaded.
- All images must be < 300 KB — compress with `sharp` before committing.

## 5) Final self-check before finishing
- [ ] No `any` in TypeScript
- [ ] No hardcoded text/images — all content from `contentStore.data`
- [ ] Single root element in every `<template>`
- [ ] `prefers-reduced-motion` handled
- [ ] All touch targets ≥ 48×48px
- [ ] Only brand colors used (see `AGENTS.md` section 4)
- [ ] No `!important` in CSS
