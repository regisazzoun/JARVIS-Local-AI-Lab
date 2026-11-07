import type { Image as NativeImageCompressor } from 'react-native-compressor';
// Web keeps the original upload URI; native compression remains in the unchanged
// .ts implementation. No native bridge is imported at web module initialization.
export const compressImage = async (
  path: string,
  _options?: NonNullable<Parameters<typeof NativeImageCompressor.compress>[1]>,
): Promise<string> => path;
