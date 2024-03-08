document.getElementById('ajouter').addEventListener('click', function() {
    var inputText = document.createElement('input');
    inputText.type = 'text';
    inputText.placeholder = 'produit';
    document.getElementById('champsSaisie').appendChild(inputText);
    
    var inputNumber = document.createElement('input');
    inputNumber.type = 'number';
    inputNumber.placeholder = 'Quantité';
    document.getElementById('champsSaisie').appendChild(inputNumber);
});
