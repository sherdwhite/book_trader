const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  entry: {
    index: [
      'core-js/stable',
      'regenerator-runtime/runtime',
      './src/index.js'
    ]
  },
  resolve: {
    extensions: ['.js', '.jsx', '.json']
  },
  optimization: {
    minimize: true,
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: '[name].css',
      experimentalUseImportModule: false
    })
  ],
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        include: path.resolve('frontend/src'),
        use: [
          {
            loader: 'babel-loader'
          }
        ]
      },
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: [
          {
            loader: 'babel-loader'
          }
        ]
      },
      {
        test: /\.css$/i,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1,
              modules: {
                exportLocalsConvention: 'camelCase',
                localIdentName: '[name]-[local]-[hash:base64:5]'
              }
            }
          },
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: [
                  'postcss-import',
                  'postcss-nested',
                ]
              }
            }
          }
        ]
      }
    ]
  },  
  output: {
    path: path.resolve(__dirname, '..', 'backend', 'static', 'build'),
    filename: 'main.js',
    library: 'voltron',
    libraryTarget: 'var'
  }
};
