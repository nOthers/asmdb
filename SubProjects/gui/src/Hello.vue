<template>
  <div class="hello-container">
    <div class="hello-grow"></div>
    <div class="hello-title user-select-none">ASM Debugger</div>
    <AssistInput class="hello-input" style="z-index:3" :icon="'device'" :type="'text'" :assist="deviceAssist" v-model="device"></AssistInput>
    <AssistInput class="hello-input" style="z-index:2" :icon="'process'" :type="'text'" :assist="processAssist" v-model="process"></AssistInput>
    <AssistInput class="hello-input" style="z-index:1" :icon="'script'" :type="'file'" :assist="scriptAssist" v-model="script"></AssistInput>
    <AnimateButton class="hello-button" :style="{marginBottom:barHeight+'px'}" :text="'start debug'" @enter="startDebug"></AnimateButton>
    <div class="hello-grow"></div>
    <a class="hello-copyright user-select-none" href="https://github.com/nOthers" target="_blank">
      <span>powered&nbsp;by&nbsp;</span>
      <span>nOthers</span>
    </a>
  </div>
</template>

<script>
import resize from '@/scripts/resize';
import asmdb from '@/scripts/asmdb';

function getBarHeight() {
  return window.outerHeight - window.innerHeight;
}

export default {
  data: function() {
    return {
      barHeight: getBarHeight(),
      device: asmdb.getToken(this.$cookies, 'device'),
      process: asmdb.getToken(this.$cookies, 'process'),
      script: asmdb.getToken(this.$cookies, 'script'),
      deviceAssist: null,
      processAssist: null,
      scriptAssist: null
    };
  },
  watch: {
    device: function() {
      this.updateDeviceAssist();
      this.updateProcessAssist();
    },
    process: function() {
      this.updateProcessAssist();
    },
    script: function() {
      this.updateScriptAssist();
    }
  },
  created: function() {
    this.updateDeviceAssist();
    this.updateProcessAssist();
    this.updateScriptAssist();
    resize.registerEvent(this);
    window.addEventListener('keydown', this.onDomKeyDown);
  },
  destroyed: function() {
    window.removeEventListener('keydown', this.onDomKeyDown);
    resize.unregisterEvent(this);
  },
  methods: {
    onResize: function() {
      requestAnimationFrames(i => {
        if (this._isDestroyed) {
          return true;
        }
        this.barHeight = getBarHeight();
        return !(i < 60);
      });
    },
    onDomKeyDown: function(event) {
      if (event.key == 'f' && !event.altKey && event.ctrlKey && !event.metaKey && !event.shiftKey) {
        this.requestFullScreen();
      } else {
        return;
      }
      event.preventDefault();
    },
    requestFullScreen: function() {
      if (document.fullscreenElement == null) {
        document.body.webkitRequestFullScreen();
      }
    },
    updateDeviceAssist: function() {
      var device = this.device;
      this.$http
        .get('/assist', {
          params: {
            type: 'device',
            value: device
          }
        })
        .then(
          resp => {
            if (device != this.device) {
              return;
            }
            this.deviceAssist = resp.data;
          },
          resp => {
            if (device != this.device) {
              return;
            }
            this.deviceAssist = [];
          }
        );
    },
    updateProcessAssist: function() {
      var device = this.device;
      var process = this.process;
      this.$http
        .get('/assist', {
          params: {
            type: 'process',
            value: process,
            context: JSON.stringify([device])
          }
        })
        .then(
          resp => {
            if (device != this.device || process != this.process) {
              return;
            }
            this.processAssist = resp.data;
          },
          resp => {
            if (device != this.device || process != this.process) {
              return;
            }
            this.processAssist = [];
          }
        );
    },
    updateScriptAssist: function() {
      var script = this.script;
      this.$http
        .get('/assist', {
          params: {
            type: 'script',
            value: script
          }
        })
        .then(
          resp => {
            if (script != this.script) {
              return;
            }
            this.scriptAssist = resp.data;
          },
          resp => {
            if (script != this.script) {
              return;
            }
            this.scriptAssist = [];
          }
        );
    },
    startDebug: function() {
      asmdb.setToken(this.$cookies, 'device', this.device);
      asmdb.setToken(this.$cookies, 'process', this.process);
      asmdb.setToken(this.$cookies, 'script', this.script);
      this.requestFullScreen();
      this.$router.replace('/world');
    }
  }
};
</script>

<style lang="less">
@import '~@/styles/theme';
@font-face {
  font-family: 'logo font';
  src: url('/static/fonts/Quantum.otf');
}

.hello-container {
  background: @color-background;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow-y: scroll;
  .hello-grow {
    flex-grow: 1;
  }
  .hello-title {
    margin-bottom: 24px;
    height: 24px;
    font-size: 24px;
    font-family: 'logo font';
    color: @color-background-darker;
  }
  .hello-input {
    margin-bottom: 8px;
    width: 333px;
  }
  .hello-button {
    margin-top: 16px;
    margin-left: 222px;
    width: 111px;
  }
  .hello-copyright {
    position: fixed;
    right: 12px;
    bottom: 8px;
    > span {
      cursor: pointer;
    }
    > span:first-child {
      font-size: 12px;
      color: @color-text-dark;
    }
    > span:last-child {
      font-size: 14px;
      color: @color-text4;
    }
  }
  .hello-copyright:hover,
  .hello-copyright:focus {
    > span {
      text-decoration: underline;
    }
  }
}
</style>
