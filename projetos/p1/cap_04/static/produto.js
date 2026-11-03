// Lê os campos do formulário e mostra os valores no console do navegador.
function mostrarProduto() {
  const nome = document.getElementById("nome").value;
  const categoria = document.getElementById("categoria").value;
  const preco = document.getElementById("preco").value;

  console.log("Nome:", nome);
  console.log("Categoria:", categoria);
  console.log("Preço:", preco);
}

// Chamada quando o formulário é enviado (onsubmit). Antes de chegar aqui, o
// navegador já conferiu required, minlength, min e step.
function cadastrarProduto(evento) {
  evento.preventDefault();
  mostrarProduto();
  console.log("Produto recebido pelo JavaScript. Ainda não existe servidor para guardá-lo.");
}
