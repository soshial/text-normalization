<?php
// this script converts 2 dictionary files' *.diff output into spelling variants database

ini_set('display_errors', 1); set_time_limit(500); 
error_reporting(E_ERROR | E_WARNING | E_PARSE | E_NOTICE);
header('Content-type: text/html; charset=utf-8');

function detect_encoding($string) { 
  static $list = array('utf-8', 'windows-1251');
 
  foreach ($list as $item) {
    $sample = iconv($item.'//IGNORE', $item, $string);
    if (md5($sample) == md5($string))
      return $item;
  }
  return null;
} // or mb_detect_encoding();

function array_has_duplicates($array){
  $dupe_array = array();
  foreach($array as $val)
    {
      if (isset($dupe_array[$val])) {$dupe_array[$val]++;} else {$dupe_array[$val] = 1;}
      if($dupe_array[$val] > 1) return $val;
    }
  return false;
}

// TODO diacritics support (jāmācos, seborrhœa, seborrhœæ): normalization and array storing!
$diff_file = file_get_contents("/home/soshial/text-normalization/hunspell/GB-ize-US.diff");
preg_match_all("/.*[\\n\\r]+/iu",$diff_file,$matches);
$temp_array = array(); $final_array = array(0 => array()); $types = array('en_US', 'en_GB'); $type_n = 0; $cnt = 0;
foreach ($matches[0] as $line)
{
  if (preg_match("/[\d,]\w[\d,]+/i",$line)) {$cnt++; $final_array[sizeof($final_array)-1][$types[$type_n]] = $temp_array; $temp_array = array(); $type_n = 1 - $type_n; $final_array[] = array();}
  elseif (preg_match("/---/i",$line)) {$final_array[sizeof($final_array)-1][$types[$type_n]] = $temp_array; $temp_array = array(); $type_n = 1 - $type_n;}
  else {preg_match("/(<|>) ([\w']+)/i",$line,$wordar); $temp_array[] = array($wordar[2], $wordar[1], metaphone($wordar[2])); }
 //if ($cnt==2) {print_r($final_array);die;}
}
$final_array[sizeof($final_array)-1][$types[$type_n]] = $temp_array;
array_shift($final_array);
$falsepos = 0; $size_incons= 0; $all=0;
print_r($final_array);
foreach ($final_array as $diff)
{
  $all++;
  // проверим равны ли размеры массивов и есть ли false positives на каждой из сторон
  if (!isset($diff['en_US']) || !isset($diff['en_GB'])) {$size_incons++;echo "0 _!\n";continue;}
  if (sizeof($diff['en_US']) != sizeof($diff['en_GB'])) $size_incons++;
  //echo sizeof($diff['en_US'])." ".sizeof($diff['en_GB'])."!\n";

  $arr_dupl1 = array(); $arr_dupl2 = array(); // arrays just for calculating whether they have duplicates
  $array_metaphone1 = array(); $array_metaphone2 = array(); // array('dramatisations'=>'TRMTSXNS',...)
  foreach($diff['en_US'] as $ar1) {$arr_dupl1[] = $ar1[2]; $array_metaphone1[$ar1[0]] = $ar1[2];}
  foreach($diff['en_GB'] as $ar2) {$arr_dupl2[] = $ar2[2]; $array_metaphone2[$ar2[0]] = $ar2[2];}
  
  // пройдёмся по всему первому массиву, ища 
  foreach($array_metaphone1 as $key => $value)
  {
    $tmpar1 = array_keys($array_metaphone1,$value);
    $tmpar2 = array_keys($array_metaphone2,$value);
    if (sizeof($tmpar1) == 1 && sizeof($tmpar2) == 1) $spelling_variants[] = array($key,array_search($value,$array_metaphone2));
    else
    {
      if (sizeof($tmpar1) == 2 && str_replace("'","",$tmpar1[0],$apost1)==str_replace("'","",$tmpar1[1],$apost2) && sizeof($tmpar2) == 2 && str_replace("'","",$tmpar2[0],$apost3)==str_replace("'","",$tmpar2[1],$apost4))
      {
        if ($apost1 == $apost3) $automatic[]=array($tmpar1[0],$tmpar2[0]);
        if ($apost1 == $apost4) $automatic[]=array($tmpar1[0],$tmpar2[1]);
        if ($apost2 == $apost3) $automatic[]=array($tmpar1[1],$tmpar2[0]);
        if ($apost2 == $apost4) $automatic[]=array($tmpar1[1],$tmpar2[1]);
      }
      else $unrecognized[] = array_merge(array_keys($array_metaphone1,$value),array_keys($array_metaphone2,$value));
    }
  }
  //if (array_has_duplicates($arr_dupl1)) {$falsepos++; echo array_has_duplicates($arr_dupl1)."____DUPL\n";continue;}
  //if (array_has_duplicates($arr_dupl2)) {$falsepos++; echo array_has_duplicates($arr_dupl2)."____DUPL\n";}
}
echo "vars:\n";print_r($spelling_variants); echo "auto:\n"; print_r($automatic); echo "unrecog:\n";print_r($unrecognized);
echo "size$size_incons falpo$falsepos of $all";