<?php
/*
этот скрипт получает текст, разбитый по принципу "каждое предложение на своей строке", пропускает через АОТ synan
и выдаёт результат для counter'a
1. запускаем генерацию всех файлов из ./in/ в ./ (utf8 -> cp1251)
2. запускаем testsynan с параметрами из ./ в ./out/ (cp1251 -> cp1251)
3. выдаём окончательный файл для резолвера (cp1251 -> ?)
4. обрабатываем резолвером (? -> ?)
*/

ini_set('display_errors', 1); set_time_limit(500); 
error_reporting(E_ERROR | E_WARNING | E_PARSE | E_NOTICE);
//header ('Content-type: text/html; charset=cp1251');
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

// 1. запускаем генерацию всех файлов из in/
echo "1. запускаем генерацию всех файлов из in/\n";

$files = file("/home/soshial/ling2/file.list");
//$list=fopen("/home/soshial/ling2/file.list",'w');
foreach ($files as $file)
{
  if (!$file || $file=="\n" || $file=="") continue;
  $text = file('/home/soshial/ling2/in/'.trim($file)); 
  $text_out = ''; $full_array = array();
  foreach ($text as $line)
  {
    if ($line && $line!="\n" && $line!="")
    {
      $line = iconv('UTF-8','cp1251//IGNORE',str_replace(array('—','―','―'),'-',str_replace(array("\n",'́'),'',trim($line))));
      $array1 = $array2 = array();
      $array1 = explode('. ',$line);
      foreach ($array1 as $part1) $array2 = array_merge($array2,explode('! ',$part1));
      foreach ($array2 as $part2) $full_array = array_merge($full_array,explode('? ',$part2));
    }
  }
  //print_r($full_array);
  file_put_contents("/home/soshial/ling2/".trim($file),implode("\n",$full_array));
  //fwrite($list,"$file\n");
}

// 2. запускаем testsynan с параметрами в out
$t = microtime();
echo "2. запускаем testsynan с параметрами в out";
if(file_exists('/home/soshial/ling2/status')) unlink('/home/soshial/ling2/status');
exec("export RML=~/ling2/rml/"); shell_exec("cd ~/ling2/");
do
{
  exec("/home/soshial/ling2/rml/Bin/TestSynan RUSSIAN /home/soshial/ling2/file.list",$output2);
  print_r($output2);
}
while(!empty($output2) && !strstr($output2[sizeof($output2)-1],'Finished'));

// 3. генерируем файл для резолвера
echo (microtime()-$t)."\n3. генерируем файл для резолвера\n";
$files = file("/home/soshial/ling2/file.list");
$numeral = iconv('UTF-8','cp1251//IGNORE',"эа/эб/эв/эг/эд/эе/Ца/Цб/Цв/Цг/Цд/Це/эж/эз/эи/эй/эк/эл/эм/эн/эо/эп/эр/эс/эт/эу/эф/эх/эц/эч/эш/юа/юб/юв/юг/Лт/юд/юе/юж/юз/юи/юй/юк/юл/юм/юн/юо/юп/юр/юс/ют/юу/юф/юх/Лу/юц/юч/ющ ");
foreach ($files as $file)
{
  $text = file('/home/soshial/ling2/out/'.trim($file));
  $out_file = fopen("/home/soshial/ling2/out/_".trim($file),'w'); $i=0;
  foreach ($text as $line)
  { //$line = iconv('cp1251','UTF-8//IGNORE',str_replace(array('—','―','―'),'-',str_replace(array("\n",'́'),'',trim($line))));
    switch ($i%4)
    {
      case 0: fwrite($out_file,$line);break;
      case 1: $words = explode(' ',$line);
	      foreach ($words as $word)
	      {
		if (is_numeric($word)) {fwrite($out_file,generate_numerals($word));}
		else fwrite($out_file,$word." ");
	      }
	      break;
      case 2: /*echo "<br/><br/>";print_r($words);echo "<br/>2#".$line.":<br/>";*/$letters = '';$space=false;$j=0; $k=0;while ($k<strlen($line)) // $j - номер слова $k - номер символа
{

  if (substr($line,$k,1)==' ' && $space == false) {$space = true;$j++;$k++;}
  elseif (substr($line,$k,1)==' ') {$k++; if (is_numeric($words[$j])) $letters.=str_repeat($numeral,sizeof(array_filter(explode(' ',generate_numerals($words[$j])))));}
  else {$space = false; if (strpos($line,' ',$k)==false) {$letters.=substr($line,$k,strlen($line)-$k);$k=strlen($line);} else
{ $letters.=substr($line,$k,strpos($line,' ',$k)-$k).' ';$k+=strpos($line,' ',$k)-$k;
}}
}fwrite($out_file,$letters."\n");break;

      case 3: break;
    }
    $i++;
  }
  fclose($out_file);
}

// 4. запускаем resolving
// todo переместить файлы в htdocs и сделать права доступа
//exec("php -f /srv/www/htdocs/aot.php",$output1);
