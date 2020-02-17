<template>
  <div class="annotation-container">
    <span v-for="(item, index) in items" :key="index" :class="item.style" v-html="item.value"></span>
  </div>
</template>

<script>
import Theme from '@/styles/theme';
import asmdb from '@/scripts/asmdb';
import InfiniteMixin from './InfiniteMixin';

function measureHeight() {
  return 18;
}

function newItem(value, ...style) {
  return {
    value: value,
    style: style
  };
}

export default {
  measureHeight: measureHeight,
  mixins: [InfiniteMixin],
  data: function() {
    return {
      items: []
    };
  },
  props: {
    address: Number,
    value: String
  },
  created: function() {
    this.needLayout.push('address', 'value');
  },
  methods: {
    onLayout: function() {
      var items = [];
      var address = '0x' + this.address.toString(16).zfill(2 * asmdb.getInstance().UNIT);
      items.push(newItem(address));
      if (this.value) {
        items.push(newItem('&nbsp;&nbsp;'));
        for (var s of this.value) {
          items.push(newItem(s == ' ' ? '&nbsp;' : s));
        }
      }
      this.items.splice(0, this.items.length, ...items);
    },
    onPreDraw: function() {
      return measureHeight();
    },
    onDraw: function(ctx) {
      ctx.font = '12px Menlo';
      var x = 0;
      var y = 12;
      x += 28;
      ctx.fillStyle = Theme.colorTextDarker;
      var address = '0x' + this.address.toString(16).zfill(2 * asmdb.getInstance().UNIT);
      ctx.fillText(address, x, y);
      x += measureLength(address.length);
      x += measureLength(2);
      if (this.value) {
        ctx.fillStyle = Theme.colorText3;
        ctx.fillText(this.value, x, y);
      }
    }
  }
};
</script>

<style lang="less">
@import '~@/styles/theme';

.annotation-container {
  height: 18px;
  > span {
    line-height: 16px;
    font-size: 12px;
    color: transparent;
    white-space: nowrap;
  }
  > span:first-of-type {
    margin-left: 28px;
  }
}
</style>
