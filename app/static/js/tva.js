function calc_taxes(price_excl, rate){
    val = parseFloat(price_excl)*100;
    val = val*rate;
    val = Math.round(val);
    return (val/100).toString();
}


function calc_price_incl(price_excl, rate){
    val = parseFloat(price_excl)
    val = val + parseFloat(calc_taxes(price_excl, rate));
    console.log(val)
    return val.toString();
}


function calc_price_excl(price_incl, rate){
    val = parseFloat(price_incl)*100;
    val = val/(1+rate);
    val = Math.round(val);
    return (val/100).toString();
}