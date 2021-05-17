const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const DjangoBridgePlugin = require('django-webpack-bridge');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const TerserJSPlugin = require('terser-webpack-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const webpack = require('webpack');

module.exports = (_env, options) => {
  if (!('VUE_DEVTOOLS' in process.env) || process.env.VUE_DEVTOOLS.length === 0) {
    process.env.VUE_DEVTOOLS = options.mode;
  }

  const config = {
    
    //context: __dirname,
    
    entry: {
      main: './app_name_vue/main.js'
    },
    
    optimization: {
      minimizer: [new TerserJSPlugin({})],
      splitChunks: {
        chunks: 'all',
      },
    },
    
    output: {
      path: '/static/app_name/',
      filename: "[name]-[contenthash].js",
      publicPath: '',
    },
    
    plugins: [
      new webpack.EnvironmentPlugin(['VUE_DEVTOOLS']),
      new CleanWebpackPlugin(),
      new VueLoaderPlugin(),
      new MiniCssExtractPlugin({
        filename: "[name]-[contenthash].css",
      }),
      new DjangoBridgePlugin(),
    ],
    
    module: {
      rules: [
        {
          test: /\.vue$/,
          loader: 'vue-loader'
        },
        {
          test: /\.m?js$/,
          exclude: /(node_modules|bower_components)/,
          use: {
            loader: 'babel-loader',
            options: {
              presets: [
                [
                  '@babel/preset-env',
                  {
                    'useBuiltIns': 'entry',
                    'corejs': 3,
                  }
                ],
              ]
            }
          }
        },
        {
          test: /\.s[ac]ss$/,
          use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"]
        },
        {
          test: /\.css$/,
          use: [MiniCssExtractPlugin.loader, "css-loader"]
        },
        {
          test: /\.(png|jpe?g|gif)$/i,
          use: [
            {
              loader: 'file-loader',
            },
          ],
        },
      ]
    },
    
    resolve: {
      extensions: ['.js', '.vue'],
      alias: {
        'vue$': 'vue/dist/vue.esm.js'
      }
    }
  };

  if (process.env.BUNDLE_ANALYZER === "True") {
    config.plugins.push(
      new BundleAnalyzerPlugin({
        analyzerHost: '0.0.0.0',
      })
    );
  }
  
  return config;
} 
