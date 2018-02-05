<?php
header("Content-Type:text/html;charset=gb2312");
ini_set('max_execution_time', '0');
require('simple_html_dom.php');

$uri = 'http://wenxue.m.iqiyi.com/book/reader-18l2gyeu1d-18l3aan9nr.html?fr=207680739';
$ch = curl_init($uri);
curl_setopt_array($ch, array(
    CURLOPT_HTTPHEADER => array('User-Agent:Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4'),
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_VERBOSE => 1
));
$curl_return = curl_exec($ch);
curl_close($ch);

$html = str_get_html($curl_return);
$title = $html->find('span[class="c-name-gap"]', 0);
$content = $html->find('section[class="m-chaper-content"]', 0);
//$next = $html->find('ul[class="m-nav-footer-list"] > li', 4);
$next = $html->find('ul[class="m-nav-footer-list"] > li', 4);
//var_dump($next->changeChapterId);

//file_put_contents("{$title->innertext}.txt", $content->plaintext);
file_put_contents(findNumber($title->innertext) . ".txt", "$title->innertext\n$content->plaintext\n");

function findNumber($str = '')
{
    $str = trim($str);
    if (empty($str)) {
        return '';
    }

    $temp = array('1', '2', '3', '4', '5', '6', '7', '8', '9', '0');
    $result = '';
    for ($i = 0; $i < strlen($str); $i++) {
        if (in_array($str[$i], $temp)) {
            $result .= $str[$i];
        }
    }

    return $result;
}