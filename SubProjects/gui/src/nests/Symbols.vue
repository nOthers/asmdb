<template>
  <div class="symbols-container">
    <div class="symbols-items symbols-libraries">
      <div v-for="(item, index) in libraries" :key="index" @click="onClickLibrary(item)" :css-selected="item==library">
        <div :style="{backgroundImage:getLibraryIcon(item)}"></div>
        <div>{{getLibraryText(item)}}</div>
      </div>
    </div>
    <div class="symbols-split"></div>
    <div class="symbols-items symbols-symbols">
      <div v-for="(item, index) in symbols" :key="index" @click="onClickSymbol(item)">
        <div :style="{backgroundImage:getSymbolIcon(item)}"></div>
        <div>{{getSymbolText(item)}}</div>
      </div>
    </div>
  </div>
</template>

<script>
import asmdb from '@/scripts/asmdb';
const VARIABLE_TYPE = ['B', 'D', 'R'];
const FUNCTION_TYPE = ['T'];

export default {
  data: function() {
    return {
      library: null,
      libraries: [],
      symbols: []
    };
  },
  methods: {
    isLibrary: function(item) {
      return item.name.endsWith('.so');
    },
    getLibraryIcon: function(item) {
      var icon;
      if (/^\/data\/app\/.*\.so$/.test(item.name)) {
        icon = 'app';
      } else {
        icon = 'lib';
      }
      var url = '/static/icons/' + icon + '.png';
      return "url('" + url + "')";
    },
    getLibraryText: function(item) {
      return asmdb.getSimpleTarget(item.name);
    },
    isSymbol: function(item) {
      if (item.value == null) {
        return false;
      }
      if (VARIABLE_TYPE.indexOf(item.type) >= 0) {
        return true;
      }
      if (FUNCTION_TYPE.indexOf(item.type) >= 0) {
        return true;
      }
      return false;
    },
    getSymbolIcon: function(item) {
      var icon;
      if (VARIABLE_TYPE.indexOf(item.type) >= 0) {
        icon = 'variable';
      }
      if (FUNCTION_TYPE.indexOf(item.type) >= 0) {
        icon = 'function';
      }
      var url = '/static/icons/' + icon + '.png';
      return "url('" + url + "')";
    },
    getSymbolText: function(item) {
      return item.name;
    },
    onUpdate: function() {
      this.updateLibraries();
    },
    updateLibraries: function() {
      this.library = null;
      this.libraries.splice(0, this.libraries.length);
      this.symbols.splice(0, this.symbols.length);
      setTimeout(() => {
        for (var item of asmdb.getInstance().getLibraries()) {
          if (this.isLibrary(item)) {
            this.libraries.push(item);
          }
        }
        //todo select pc and foucs scroll
      });
    },
    onClickLibrary: function(item) {
      this.library = item;
      this.updateSymbols();
    },
    updateSymbols: function() {
      this.symbols.splice(0, this.symbols.length);
      var library = this.library;
      if (library != null) {
        asmdb.getInstance().nm(library.name, symbols => {
          if (this.library != library) {
            return;
          }
          for (var item of symbols) {
            if (this.isSymbol(item)) {
              this.symbols.push(item);
            }
          }
        });
      }
    },
    onClickSymbol: function(item) {
      this.$emit('clickitem', this.library.value + item.value);
    }
  }
};
</script>

<style lang="less">
@import '~@/styles/theme';

.symbols-container {
  height: 350px;
  display: flex;
  .symbols-items {
    flex-basis: 0;
    height: 100%;
    overflow-y: scroll;
    > div {
      height: 22px;
      display: flex;
      align-items: center;
      cursor: pointer;
      > div {
        cursor: pointer;
      }
      > div:first-child {
        flex-shrink: 0;
        margin-left: 12px;
        width: 16px;
        height: 16px;
        background-size: 16px 16px;
        background-repeat: no-repeat;
        background-position: center center;
      }
      > div:last-child {
        margin-left: 8px;
        font-size: 12px;
        color: @color-text;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
      }
    }
    > div:hover,
    > div[css-selected] {
      background: @color-background-selection;
    }
  }
  .symbols-libraries {
    flex-grow: 1;
  }
  .symbols-symbols {
    flex-grow: 2;
  }
  .symbols-split {
    width: 1px;
    height: 100%;
    background: @color-border-light;
  }
}
</style>
