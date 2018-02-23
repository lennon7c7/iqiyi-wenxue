<?php
header("Content-type: text/html; charset=utf-8");
ini_set('max_execution_time', '0');
require('simple_html_dom.php');

$url = isset($_REQUEST['url']) ? $_REQUEST['url'] : '';
$not_merge = isset($_REQUEST['not_merge']) ? true : false;
if ($url) {
    $domain = 'wenxue.m.iqiyi.com';
    $url = str_replace('wenxue.iqiyi.com', $domain, $url);
    $url_array = explode('-', $url);
    $chapter_id = array_pop($url_array);
    $chapter_id = str_replace('.html', '', $chapter_id);
    $book_id = array_pop($url_array);
    do {
        $url = "$domain/book/reader-$book_id-$chapter_id.html";
        $ch = curl_init($url);
        curl_setopt_array($ch, array(
            CURLOPT_HTTPHEADER => array($_REQUEST['curl_agent']),
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_VERBOSE => 1
        ));
        curl_setopt($ch, CURLOPT_COOKIE, $_REQUEST['curl_cookie']);
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


        if (!$not_merge) {
            // output one file
            $filename = "all.txt";
            file_put_contents($filename, "$title$content\n", FILE_APPEND);
        } else {
            $filename = explode(' ', $title);
            $filename = findNumber($filename[0]) . '.txt';
            file_put_contents($filename, "$title$content\n");
        }

        $chapter_id = '';
        $next = $html->find('a[class="c-link"]', 4);
        if ($next->changechapterid) {
            $chapter_id = $next->changechapterid;
        }
    } while ($chapter_id);

    echo 'done';
}


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

?>

<form method="post">
    <p>url:
        <input type="text" name="url" style="width: 100%" value="http://wenxue.iqiyi.com/book/reader-18l2h82x4d-18l3d6hr57.html"/>
    </p>
    <p>user agent:
        <textarea name="curl_agent" style="width: 100%">User-Agent:Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4</textarea>
    </p>
    <p>cookie:
        <textarea name="curl_cookie" style="width: 100%" rows="5">bd_token=tRqfm0plD8N20kjtTMpPZs kliVzg2stYokk/U8RDD5dJua73QX75QiQL0I/BkqLxRIvN7rAfw4; bd_uid=D29180091A62A1CFA6A25BBEFC2B67D5; bd_cpid=10002; bd_gid=4305831314; litera_h5_prev_page=http%3A%2F%2Fwenxue.iqiyi.com%2Fbook%2Fdetail-18l2h10ca5.html; QC006=da0c96237b6b460dc27a67d824393c18; sourceFromType=baidu; QC005=1af75b059564a9e5cda46d3b588bbc4f; QC154=true; __dfp=a018d246d3b57f4b008e4079924b66927ac826fb9f103baf6e67ae199f019b679d@1519559471525@1516967471525; QC153=http%3A%2F%2Fwenxue.iqiyi.com%2Fbook%2Fdetail-18l2h10ca5.html; litera_h5_reffer=http%3A%2F%2Fwenxue.iqiyi.com%2Fbook%2Fdetail-18l2h10ca5.html; litera_h5_OrderInCurrentPage=667; cookie_readingProgress=%7B%2218l2h1252p%22%3A%2218l2al6dbf%22%2C%2218l2gyeu1d%22%3A%2218l3ad45lv%22%2C%2218l2h10ca5%22%3A%2218l2b79v8z%22%7D</textarea>
    </p>

    <button type="submit">Submit</button>
</form>

<?php if (!empty($filename) && file_exists($filename)) { ?>
    <a href="<?php echo $filename; ?>" id="download" download>all.txt</a>

    <script type="text/javascript">
        //document.getElementById('download').click();
    </script>
<?php } ?>
