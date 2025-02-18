const path = require('path')
const HtmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
    mode: "production",
    entry: [
        './src/static_assets/js/fl-chart.js'
    ],
    output: {
        filename: 'staticfiles/fl-chart.js',
    },
    plugins: [
        new HtmlWebpackPlugin()
    ],
}
