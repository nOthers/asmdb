<template>
  <div class="frame-container" :style="style">
    <slot></slot>
  </div>
</template>

<script>
import Animation from '@/scripts/animation';
import resize from '@/scripts/resize';

function getChildrenHeight(el) {
  var sum = 0;
  for (var node of el.childNodes) {
    sum += node.clientHeight;
  }
  return sum;
}

export default {
  data: function() {
    return {
      anim: new Animation((v, t) => {
        var y = 1 - Math.abs(v - t);
        var x = 1 - Math.pow(1 - y, 1 / 2);
        var k = 2 - 2 * x;
        var d = 0;
        if (this.$el) {
          d = getChildrenHeight(this.$el) / screen.height;
        }
        return Math.max(k, 0.01) / (147 + 224 * d);
      })
    };
  },
  props: {
    show: Boolean
  },
  watch: {
    show: function(newValue, oldValue) {
      this.anim.$target(newValue ? 1 : 0);
      if (newValue) {
        this.$children[0].onUpdate();
      }
    }
  },
  computed: {
    style: function() {
      this.$nextTick(() => {
        resize.dispatchEvent();
      });
      var t = this.anim.value;
      if (t == 0) {
        return { display: 'none' };
      } else if (t == 1) {
        return {};
      } else {
        var h = 0;
        if (this.$el) {
          h = getChildrenHeight(this.$el);
        }
        var height = h * t;
        return { height: height + 1 + 'px' };
      }
    }
  }
};
</script>

<style lang="less">
@import '~@/styles/theme';

.frame-container {
  overflow-y: hidden;
  border-bottom: 1px solid @color-border-light;
}
</style>
