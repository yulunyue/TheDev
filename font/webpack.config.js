const HtmlWebpackPlugin = require('html-webpack-plugin');

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
            { test: /\.(t|j)sx?$/, use: { loader: 'ts-loader', options: { transpileOnly: true } }, exclude: /node_modules/ },

            // addition - add source-map support
            { enforce: "pre", test: /\.js$/, exclude: /node_modules/, loader: "source-map-loader" },
            { test: /\.css$/, use: ["style-loader", "css-loader"], exclude: /node_modules/ },
            {
                test: /\.(jpg|png|gif)$/,
                type: 'asset/resource',
            }
        ]
    },
    plugins: [new HtmlWebpackPlugin()],
    externals: {

    },
    devServer:{
        port: 48080
    },
    // addition - add source-map support
    devtool: "source-map"
}