const path = require('path')
const HtmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
    mode: "production",
    entry: [
        './src/static_assets/js/fl-table.js'
    ],
    output: {
        filename: 'staticfiles/fl-table.js',
    },
    plugins: [
        new HtmlWebpackPlugin()
    ],
}
