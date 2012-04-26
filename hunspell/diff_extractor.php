<?php
// this script converts 2 dictionary files' *.diff output into spelling variants database

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

// tells whether an array has any duplicates inside
function array_has_duplicates($array){
  $dupe_array = array();
  foreach($array as $val)
    {
      if (isset($dupe_array[$val])) {$dupe_array[$val]++;} else {$dupe_array[$val] = 1;}
      if($dupe_array[$val] > 1) return $val;
    }
  return false;
}

// gives us the number of the next word_id to be added
function next_word_id($word)
{
  $query_result = mysql_query("SELECT * FROM word_equivalents_en WHERE word_spelling = '$word'");
  if (!$query_result) die('Ошибка выполнения запроса:' . mysql_error());
  $result_array = mysql_fetch_assoc($query_result);
  if ($result_array) return $result_array['word_id'];
  else
  {
    $query_result = mysql_query("SELECT MAX(word_id) FROM word_equivalents_en");
    return mysql_result($query_result,0)+1;
  }
}

// TODO jāmācos, seborrhœa, seborrhœæ
$diff_file = file_get_contents("/home/soshial/text-normalization/hunspell/GB-ize-GB-ise.diff"); // input aspell diff
preg_match_all("/.*[\\n\\r]+/iu",$diff_file,$matches);
$temp_array = array(); $final_array = array(0 => array()); $types = array('en_GB', 'en_US'); $type_n = 1; $cnt = 0;
// processing the lines
foreach ($matches[0] as $line)
{
  // 118570c118541,118542 and 115673a115679 are delimeters between diffs
  if (preg_match("/[\d,][a-z][\d,]+/i",$line)) {$cnt++; $final_array[sizeof($final_array)-1][$types[$type_n]] = $temp_array; $temp_array = array(); $type_n = 0; $final_array[] = array();}
  // --- is for delimetering two files in one diff
  elseif (preg_match("/---/i",$line)) {$final_array[sizeof($final_array)-1][$types[$type_n]] = $temp_array; $temp_array = array(); $type_n = 1;}
  // the word starting with < or > sign
  else { preg_match("/(<|>) ([\p{L}'-]+)/iu",$line,$wordar); $temp_array[] = array($wordar[2], $wordar[1], metaphone($wordar[2])); }
}
// preparing array
$final_array[sizeof($final_array)-1][$types[$type_n]] = $temp_array; array_shift($final_array);

$spelling_variants = array(); // absolute matching variants
$unrecognized = array(); // array of too ambiguous matches
$automatic = array();  // automaticly disambiguated matches
$size_incons = 0; // number of non-matching between two files inside one diff
$all = 0; // $final_array counter

foreach ($final_array as $diff)
{
  $all++; $unrecog = array(); // 
  if (!isset($diff['en_US']) || !isset($diff['en_GB']) || sizeof($diff['en_US']) != sizeof($diff['en_GB'])) $size_incons++; // counting number of non-matches

  $arr_dupl1 = array(); $arr_dupl2 = array(); // arrays just for calculating whether they have duplicates
  $array_metaphone1 = array(); $array_metaphone2 = array(); // array('dramatisations'=>'TRMTSXNS',...)
  foreach($diff['en_GB'] as $ar1) {$arr_dupl1[] = $ar1[2]; $array_metaphone1[$ar1[0]] = $ar1[2];}
  foreach($diff['en_US'] as $ar2) {$arr_dupl2[] = $ar2[2]; $array_metaphone2[$ar2[0]] = $ar2[2];}

  // we go through the first array, detecting it's matches in the second
  foreach($array_metaphone1 as $key => $value)
  {
    $tmpar1 = array_keys($array_metaphone1,$value);
    $tmpar2 = array_keys($array_metaphone2,$value);
    // full metaphone match: 1 to 1
    if (sizeof($tmpar1) == 1 && sizeof($tmpar2) == 1)
    {
      $spelling_variants[] = array("en_GB"=>$key,"en_US"=>array_search($value,$array_metaphone2));
      unset($array_metaphone2[array_search($value,$array_metaphone2)]); // unsetting found matches for latter easier processing of remaining ones
      unset($array_metaphone1[$key]);
    }
    else
    {
      // automatic disambiguation for case of apostrophies and plurals
      if (sizeof($tmpar1) == 2 && str_replace("'","",$tmpar1[0],$apost1)==str_replace("'","",$tmpar1[1],$apost2) && sizeof($tmpar2) == 2 && str_replace("'","",$tmpar2[0],$apost3)==str_replace("'","",$tmpar2[1],$apost4))
      {
        if ($apost1 == $apost3) {$automatic[]=array("en_GB"=>$tmpar1[0],"en_US"=>$tmpar2[0]); unset($array_metaphone1[$tmpar1[0]]); unset($array_metaphone2[$tmpar2[0]]);}
        if ($apost1 == $apost4) {$automatic[]=array("en_GB"=>$tmpar1[0],"en_US"=>$tmpar2[1]); unset($array_metaphone1[$tmpar1[0]]); unset($array_metaphone2[$tmpar2[1]]);}
        if ($apost2 == $apost3) {$automatic[]=array("en_GB"=>$tmpar1[1],"en_US"=>$tmpar2[0]); unset($array_metaphone1[$tmpar1[1]]); unset($array_metaphone2[$tmpar2[0]]);}
        if ($apost2 == $apost4) {$automatic[]=array("en_GB"=>$tmpar1[1],"en_US"=>$tmpar2[1]); unset($array_metaphone1[$tmpar1[1]]); unset($array_metaphone2[$tmpar2[1]]);}
      }
      else
      {
        $unrecog[] = array("en_GB"=>array_keys($array_metaphone1,$value),"en_US"=>array_keys($array_metaphone2,$value));
        foreach(array_keys($array_metaphone2,$value) as $k=>$v) unset($array_metaphone2[$k]);
        foreach(array_keys($array_metaphone1,$value) as $k=>$v) unset($array_metaphone1[$k]);
      }
    }
  }
  // adding all unrecognized from the first array $unrecog
  $unrecognized = array_merge($unrecognized, $unrecog);
  // adding all remaining unrecognized ones the second arrays $array_metaphone2 and $array_metaphone1
  $unrecognized[] = array("en_US"=>array_keys($array_metaphone2),"en_GB"=>array_keys($array_metaphone1));
}

echo "spelling variants:\n"; print_r($spelling_variants); echo "auto:\n"; print_r($automatic); echo "unrecog:\n";print_r($unrecognized);

// adding to the database
$db = mysql_connect("192.168.2.101","builder","builderpass");
mysql_select_db("builder",$db);

foreach($spelling_variants as $variant)
{
  $word0 = mysql_real_escape_string($variant["en_GB"]);$word1 = mysql_real_escape_string($variant["en_US"]);
  $next_word_id = min(next_word_id($word0),next_word_id($word1));
  $result = mysql_query("INSERT INTO word_equivalents_en (lang,word_id,word_spelling,meta_info,principal,relation)
                              VALUES ('en',$next_word_id,'$word0','ize',1,1), 
                                     ('en',$next_word_id,'$word1','ise',0,1)");
}//wo_diac //with_diac
foreach($automatic as $variant)
{
  $word0 = mysql_real_escape_string($variant["en_GB"]);$word1 = mysql_real_escape_string($variant["en_US"]);
  $next_word_id = min(next_word_id($word0),next_word_id($word1));
  $result = mysql_query("INSERT INTO word_equivalents_en (lang,word_id,word_spelling,meta_info,principal,relation)
                              VALUES ('en',$next_word_id,'$word0','ize',1,1),
                                     ('en',$next_word_id,'$word1','ise',0,1)");
}
foreach($unrecognized as $variant)
{
  
  $next_word_id = next_word_id(mysql_real_escape_string($variant['en_GB'][0]));
  foreach ($variant['en_GB'] as $var) {$next_word_id = min(next_word_id(mysql_real_escape_string($var)),$next_word_id);}
  foreach ($variant['en_GB'] as $var)
  {
      $word = mysql_real_escape_string($var);
      mysql_query("INSERT INTO word_equivalents_en (lang,word_id,word_spelling,meta_info,principal,relation)
                              VALUES ('en',$next_word_id,'$word','ize',-1,1)");
  }
  foreach ($variant['en_US'] as $var) {$next_word_id = min(next_word_id(mysql_real_escape_string($var)),$next_word_id);}
  foreach ($variant['en_US'] as $var)
  {
      $word = mysql_real_escape_string($var);
      mysql_query("INSERT INTO word_equivalents_en (lang,word_id,word_spelling,meta_info,principal,relation)
                              VALUES ('en',$next_word_id,'$word','ise',-1,1)");
  }
}

