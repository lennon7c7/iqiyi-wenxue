<?php
header("Content-type: text/html; charset=utf-8");
ini_set('max_execution_time', '0');
require('simple_html_dom.php');

$url = isset($_REQUEST['url']) ? $_REQUEST['url'] : '';
$merge = isset($_REQUEST['merge']) ? true : false;
//$url = 'http://wenxue.m.iqiyi.com/book/reader-18l2gyeu1d-18l3ad45lv.html';
if (empty($url)) {
    die('url is empty!');
}

$domain = 'wenxue.m.iqiyi.com';
$url = str_replace('wenxue.iqiyi.com', $domain, $url);
$url_array = explode('-', $url);
$chapter_id = array_pop($url_array);
$chapter_id = str_replace('.html', '', $chapter_id);
$book_id = array_pop($url_array);
do {
    $url = "$domain/book/reader-$book_id-$chapter_id.html?fr=207680739";
    $ch = curl_init($url);
    curl_setopt_array($ch, array(
        CURLOPT_HTTPHEADER => array('User-Agent:Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4'),
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_VERBOSE => 1
    ));
    $curl_return = curl_exec($ch);
    curl_close($ch);

    $html = str_get_html($curl_return);
    $title = $html->find('span[class="c-name-gap"]', 0)->innertext;

    //带HTML
    //$content = $html->find('section[class="m-chaper-content"]', 0)->plaintext;

    //不带HTML
    $content = '';
    foreach ($html->find('section[class="m-chaper-content"] > p') as $key => $value) {
        $content .= "$value->innertext\n";
    }

    $filename = explode(' ', $title);
    $filename = findNumber($filename[0]) . '.txt';

    if ($merge) {
        // output one file
        file_put_contents("txt/all.txt", "$title$content\n", FILE_APPEND);
    } else {
        file_put_contents("txt/$filename", "$title$content\n");
    }

    $chapter_id = '';
    $next = $html->find('a[class="c-link"]', 4);
    if ($next->changechapterid) {
        $chapter_id = $next->changechapterid;
    }
} while ($chapter_id);

die('done');

/**
 * find number from string
 * @param string $str
 * @return string
 */
function findNumber($str = '')
{
    $str = trim($str);
    if (empty($str)) {
        return '0';
    }

    $temp = array('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十');
    $result = '';
    for ($i = 0; $i < strlen($str); $i++) {
        if (in_array($str[$i], $temp)) {
            $result .= $str[$i];
        }
    }

    return $result;
}