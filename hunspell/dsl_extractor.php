<?php
// this script converts regex output file into spelling variants database

ini_set('display_errors', 1); set_time_limit(500); 
error_reporting(E_ERROR | E_WARNING | E_PARSE | E_NOTICE);
header('Content-type: text/html; charset=utf-8');

// returns string encoding
function detect_encoding($string) { 
  static $list = array('utf-8', 'windows-1251');
 
  foreach ($list as $item) {
    $sample = iconv($item.'//IGNORE', $item, $string);
    if (md5($sample) == md5($string))
      return $item;
  }
  return null;
} // or mb_detect_encoding();

// gives us the number of the next word_id to be added
function next_word_id($word)
{
  $query_result = mysql_query("SELECT * FROM word_equivalents_ru WHERE word_spelling = '$word'");
  if (!$query_result) die('Ошибка выполнения запроса:' . mysql_error());
  $result_array = mysql_fetch_assoc($query_result);
  if ($result_array) return $result_array['word_id'];
  else
  {
    $query_result = mysql_query("SELECT MAX(word_id) FROM word_equivalents_ru");
    return mysql_result($query_result,0)+1;
  }
}

$diff_file = file_get_contents("/home/soshial/text-normalization/hunspell/file_final.txt"); // input pre-processed dsl
$diff_file = str_replace("\n","",$diff_file);
preg_match_all("/@#\\$(\p{L}*)\|([\p{L} ~{}:*-]*)\|(.+?)\\$#@/iu",$diff_file,$matches);

$spelling_variants = array(); // absolute matching variants
$unrecognized = array(); // array of too ambiguous matches
$automatic = array();  // automaticly disambiguated matches

// adding to the database
$db = mysql_connect("192.168.2.101","builder","builderpass");
mysql_select_db("builder",$db);
$cnt = 0;

foreach($matches[0] as $match)
{
  $meta1 = "__1"; $meta0 = "__2"; $relation = 1;
  echo $word0 = mysql_real_escape_string($matches[1][$cnt]); echo "_";
  $word1_tmp = str_replace(array("{a}","{b}"),"",$word1_tmp = $matches[2][$cnt],$amount1);
  if ($amount1 !== 0) $relation = 3;
  preg_match("/{(3|4)([\p{L} ~{}:*-]*)}/iu",$word1_tmp,$match);
  echo $word1 = mysql_real_escape_string($word1_tmp);
  preg_match_all("/\[p\]([^[]*)\[\/p\]/iu",$matches[3][$cnt],$meta); $meta0 = implode(",",$meta[1]);
  if (strstr($word1,"~"))
  {
    #echo "const___".$word0.$word1.str_replace("~",$word0,$word1)."<br/>\n";
    $word1 = str_replace("~",$word0,$word1);
  }
  echo "<br/>";
  if (strstr($word0,"~") !== false) die("$word0 contains ~");
  $next_word_id = min(next_word_id($word0),next_word_id($word1));
  $result1 = mysql_query(" INSERT INTO word_equivalents_ru (lang,word_id,word_spelling,meta_info,principal,relation)
                              VALUES ('ru',$next_word_id,'$word0','$meta0',0,$relation)
                              ON DUPLICATE KEY UPDATE meta_info = CONCAT(meta_info,'$meta0')");
  $result2 = mysql_query("INSERT INTO word_equivalents_ru (lang,word_id,word_spelling,meta_info,principal,relation)
                              VALUES ('ru',$next_word_id,'$word1','$meta1',1,1)
                              ON DUPLICATE KEY UPDATE meta_info = CONCAT(meta_info,'$meta1')");
  if (!$result1 || !$result2) die('Ошибка выполнения запроса:' . mysql_error());
  $cnt++;
}
