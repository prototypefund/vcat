require('dotenv').config()

const webpack = require('webpack')
const path = require('path')
const UglifyJsPlugin = require('uglifyjs-webpack-plugin')
// const CleanWebpackPlugin = require('clean-webpack-plugin')

module.exports = {
  entry: {
    main: './app/index.js',
  },
  output: {
    path: path.resolve(__dirname, 'static'),
    filename: 'app.js',
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': '"production"',
      'process.env.S3_HOST': '"' + process.env.S3_HOST + '"',
      'process.env.API_HOST': '""',
    }),
    new UglifyJsPlugin(),
    new webpack.optimize.AggressiveMergingPlugin()
  ],
  devtool: 'inline-source-map',
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      },
      {
        test: /\.js$/,
        include: path.resolve(__dirname, 'app'),
        exclude: /(node_modules|bower_components|build)/,
        loader: 'babel-loader',
        options: {
          presets: ['env'],
          plugins: [
            require('babel-plugin-transform-runtime'),
            require('babel-plugin-transform-es2015-arrow-functions'),
            require('babel-plugin-transform-object-rest-spread'),
            require('babel-plugin-transform-class-properties'),
            require('babel-plugin-transform-react-jsx'),
          ]
        }
      }
    ]
  },
};
