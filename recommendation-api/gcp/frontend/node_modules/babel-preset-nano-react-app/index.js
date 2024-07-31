module.exports = function() {
  return {
    plugins: [
      ["@babel/plugin-transform-runtime", { regenerator: true }],
      ["@babel/plugin-proposal-class-properties", { loose: true }],
      ["@babel/plugin-transform-react-jsx", { pragmaFrag: "React.Fragment" }],
    ],
  };
};
