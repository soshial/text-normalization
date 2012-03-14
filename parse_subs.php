<?php
// нужен файл с description всех субтитров и функция очистки от тегов strip_tags_smart
ini_set('display_errors', 1); set_time_limit(500); 
error_reporting(E_ERROR | E_WARNING | E_PARSE | E_NOTICE);
header('Content-type: text/html; charset=utf-8');
include 'strip_tags_smart.php';
function detect_encoding($string) { 
  static $list = array('utf-8', 'windows-1251');
 
  foreach ($list as $item) {
    $sample = iconv($item.'//IGNORE', $item, $string);
    if (md5($sample) == md5($string))
      return $item;
  }
  return null;
} // or mb_detect_encoding();

function uncompress($srcName, $dstName) {
    $string = implode("", gzfile($srcName));
    $fp = fopen($dstName, "w");
    fwrite($fp, $string, strlen($string));
    fclose($fp);
}

$subs_file = file_get_contents("export.txt"); $subs = array();
preg_match_all("/.*[\\n\\r]+/iu",$subs_file,$matches);
foreach ($matches[0] as $line)
{
  $subtitle = explode("\t",$line);
  if (!is_numeric($subtitle[1])) continue;

  uncompress('/home/soshial/subs/opensubtitles/'.$subtitle[1].'.gz','/home/soshial/subs/opensubtitles2/'.$subtitle[1].'.srt');
  $sub_text = file_get_contents('/home/soshial/subs/opensubtitles2/'.$subtitle[1].'.srt');

  
  if (detect_encoding($sub_text) == 'windows-1251') $sub_text = strip_tags_smart(iconv('windows-1251', 'UTF-8//IGNORE', $sub_text)); // изменяем кодировку на юникод, и вычищаем от тегов
  $sub_text = preg_replace('/\s*\d+\r\n\d\d:\d\d:\d\d,\d+ --> \d\d:\d\d:\d\d,\d+/i','',$sub_text,-1,$count); // вырезаем временные метки
  $sub_text = preg_replace('/\.{2,}/i','…',$sub_text,-1,$count); // заменяем многоточия

  /* склеиваем текст */
  $sub_text = preg_replace("/([^!…\?_][a-z0-9а-яё])(\s)*\\r\\n(\s)*([…«\"\-]{0,1}(\s)*[a-zа-яё]{1,}[^\)])/u",'$1 $4',$sub_text,-1,$count);
  // ориентация на отсутствие препинаний в конце первого параграфа и на строчные в начале второго п.,
  // где перед буквами могут находиться кавычки: «" и дефис
  // предполагается автоматическое объединение

  $sub_text = preg_replace("/([^!…\?_][a-z0-9А-яё,;—–\-\»\)IVX])(\s)*\\r\\n(\s)*([«\(\[\"\-–—=…]{0,1}(\s)*[a-z0-9а-яё\?\!…\"]+[^\)])/u",'$1 $4',$sub_text,-1,$count);
  // ориентация на отсутствие точки в конце первого параграфа и на строчные в начале второго п.,
  // где перед буквами и цифрами могут находиться кавычки: «", дефис и скобки: ([
  // отключены скобки после первого символа второго п. дабы не цеплять пронумерованные списки

  $sub_text = preg_replace("/([a-zа-яё\d\w][\?!…»\"“])(\s){0,}\\r\\n(\s){0,}([«\"\(\[\-–—\.,…<]{0,1}(\s){0,}(\s){0,1}[a-zа-яё…\"«][a-zа-яё\d])/u",'$1 $4',$sub_text,-1,$count);
  // здесь в конце строки может быть всё что угодно (например, прямая речь, потом тире и описание того, кто говорит),
  // но опять же только не точка
  // второй параграф может начинаться только с маленькой буквы, т.е. предполагается слияние

  file_put_contents('/home/soshial/subs/opensubtitles4/'.$subtitle[1].'.txt',$sub_text);//die($subtitle[1]);
}