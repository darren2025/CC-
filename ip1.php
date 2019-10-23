<?php
$data = file_get_contents('http://www.66ip.cn/mo.php?sxb=&tqsl=9998&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=');

$regx = '/(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\:+\d+/';
preg_match_all($regx, $data, $echo);


foreach ($echo[0] as $key => $value) {

	file_put_contents('./20.txt', $value . PHP_EOL, FILE_APPEND);
	
}
