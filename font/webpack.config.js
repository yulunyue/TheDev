const HtmlWebpackPlugin = require('html-webpack-plugin');
const path = require('path');
module.exports = {
    // change to .tsx if necessary
    entry: './src/app.ts',
    output: {
        filename: './bundle.js'
    },
    mode: "development",
    resolve: {
        extensions: [".ts", ".js"],
        // alias: {
        //     '@': path.resolve(__dirname, "src")
        // },
    },
    module: {
        rules: [
            // changed from { test: /\.jsx?$/, use: { loader: 'babel-loader' }, exclude: /node_modules/ },
            { test: /\.(t|j)sx?$/, use: { loader: 'ts-loader' }, exclude: /node_modules/ },

            // addition - add source-map support
            { enforce: "pre", test: /\.js$/, exclude: /node_modules/, loader: "source-map-loader" },
            { test: /\.css$/, use: ["style-loader", "css-loader"], exclude: /node_modules/ },
            {
                test: /\.(jpg|png|gif)$/,
                use: {
                    loader: 'file-loader',
                    options: {
                        name: '[path][name].[hash].[ext]',
                    },
                },
            }
        ]
    },
    plugins: [new HtmlWebpackPlugin()],
    externals: {

    },
    // addition - add source-map support
    devtool: "source-map"
}