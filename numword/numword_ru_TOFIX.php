<?php
$mas = array( "", "один", "два", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять", "десять" );
$mas1 = array( "десять", "одиннадцать", "двенадцать", "тринадцать", "четырнадцать","пятнадцать", "шестнадцать", "семнадцать", "восемнадцать", "девятнадцать" );
$mas2 = array("двадцать", "тридцать", "сорок", "пятьдесят", "шестьдесят", "семьдесят", "восемьдесят", "девяносто");
$mas3 = array("сто","двести", "триста", "четыреста", "пятьсот", "шестьсот", "семьсот", "восемьсот", "девятьсот");
//$mas4 = array( "ноль", "одна", "две", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять", "десять");
//$mas5 = array( "тысяча", "тысячи", "тысяч");
$mas_large = array('','тысяча ','миллион ','миллиард ','триллион ','квадриллион ');
function m1($chislo) //0-10
{
  global $mas;
  return $mas[$chislo];
}

function m2($chislo)  //10-19
{
  global $mas1;
  return $mas1[$chislo%10];
}

function m3($chislo)  //21-99
{
  global $mas2;
  return $mas2[$chislo/10-2];
}

function m4($chislo)  //100-999
{
  global $mas3;
  return $mas3[$chislo/100-1];
}

function m5($chislo)
{
  global $mas,$mas5;
  if (substr($chislo,0,-3)!=1) return generate_numerals(substr($chislo,0,-3)).' тысяча';
  else return 'тысяча';
}

function m($chislo)  //функция, которая выбирает число по его типу
{
  if($chislo >= 0 && $chislo < 10)
  return m1($chislo);
  if($chislo >= 10 && $chislo < 20)
  return m2($chislo);
  if($chislo >= 20 && $chislo < 100)
  return m3($chislo);
  if($chislo >= 100 && $chislo < 1000)
  return m4($chislo);
}
function generate_numerals($chislo)
{//die($chislo);
  // ищешь в строке число и присваиваешь переменной $chislo1
  $str = ''; global $mas_large;$rank = ''; $trigger = false;
  for($i=0;$i<strlen($chislo);$i++)
  {
    $cifra=substr($chislo,$i,1);
    $rank_int = strlen($chislo)-$i; // у цифры 1 числа 123 ранк 3
    $cifra*=pow(10,($rank_int-1)%3);
    $rank_str = $mas_large[floor(($rank_int-1)/3)];
    if ((strlen($chislo)-$i)%3==2 && substr($chislo,$i,1)==1) {$str.=m(substr($chislo,$i,2)).' '; $trigger=true;}
    elseif (!$trigger) {$str.=m($cifra)." ";} else{ $trigger = false;}
    if ($rank_int%3==1) {$str .= $rank_str;}
  }return iconv('UTF-8','cp1251//IGNORE',$str);
// заменяешь найденное число на $str
} 
