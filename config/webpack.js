var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

module.exports = {
  context: __dirname,

  entry: '../src/main.js', // これがエントリーポイント

  output: { // コンパイルされたファイルの設定
      path: path.resolve('../assets/bundles/'),
      filename: "[name]-[hash].js",
  },

  plugins: [
    new BundleTracker({filename: '../webpack-stats.json'}),
  ],

  resolve: {
    extensions:['.ts','.js'],
    alias: {
      'vue': path.resolve('../node_modules/vue/dist/vue.js'),
    }
  },
  module: {
      rules: [
          {
              // 拡張子が.tsで終わるファイルに対して、TypeScriptコンパイラを適用する
              test:/\.ts$/,
              loader:'ts-loader'
          }
      ]
  }
}
