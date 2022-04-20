module.exports = {
  parser: '@babel/eslint-parser',
  parserOptions: {
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true
    }
  },
  env: {
    browser: true,
    es6: true,
    jest: true,
    node: true
  },
  plugins: [
    'react',
    'react-hooks'
  ],
  extends: [ 'eslint:recommended', 'plugin:react/recommended'],
  rules: {
    'indent': [ 'error', 2, { 'SwitchCase': 1 } ],
    'no-console': [ 'off' ],
    'react-hooks/exhaustive-deps': 'warn',
    'react-hooks/rules-of-hooks': 'error',
    'react/jsx-uses-react': [ 'error' ],
    'react/jsx-uses-vars': [ 'error' ],
    'react/prop-types': [ 'off' ],
    'react/react-in-jsx-scope': [ 'off' ],
  },
  settings: {
    react: {
      version: 'detect'
    }
  }
};
