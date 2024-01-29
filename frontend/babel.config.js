module.exports = {
  presets: [
    ['@babel/preset-env', { corejs: 3, useBuiltIns: 'entry' }],
    ['@babel/preset-react', { runtime: 'automatic' }]
  ],
  plugins: [
    '@babel/plugin-transform-runtime',
  ]
}