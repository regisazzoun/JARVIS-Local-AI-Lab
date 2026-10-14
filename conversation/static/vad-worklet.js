'use strict';
class JarvisCapture extends AudioWorkletProcessor {
  process(inputs,outputs) {
    const channel=inputs[0]?.[0];
    if(channel)this.port.postMessage(channel.slice());
    return true;
  }
}
registerProcessor('jarvis-capture',JarvisCapture);
