import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.physicswithdhanya.thumbnailstudio',
  appName: 'Thumbnail Studio',
  webDir: '../static',
  server: {
    androidScheme: 'http'
  }
};

export default config;
