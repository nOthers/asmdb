<template>
  <div class="frame-container">
    <slot></slot>
  </div>
</template>

<script>
export default {};
</script>

<style lang="less">
@import '~@/styles/theme';

.frame-container {
  border-bottom: 1px solid @color-border-light;
}
</style>
