<?php

 $data = file_get_contents('https://www.kuaidaili.com/free/intr/1/');
        preg_match('/\d{4}(?=<\/a><\/li><li>页<\/li><\/ul>)/', $data, $pega);
        $oag = $pega[0];

        for ($i=1; $i <=$oag ; $i++) {
            // 延时一秒
            sleep(1);
            // 取得数据
            $data = file_get_contents("https://www.kuaidaili.com/free/intr/$i/");
            // 第一次 匹配tbody
            preg_match_all('/<tbody[.\s\S]*?>[.\s\S]*?<\/tbody>/', $data, $tbody);
            // 第二次 匹配 tr标签
            preg_match_all('/<tr[.\s\S]*?>[.\s\S]*?<\/tr>/', $tbody[0][0], $tr);
            // 这里需要遍历 
            foreach ($tr[0] as  $value) {
                // 第三次 匹配 td
                preg_match_all('/<td[.\s\S]*?>[.\s\S]*?<\/td>/', $value, $td);

                // 匹配IP
                preg_match('/<td[^>]+>(.*?)<\/td>/', $td[0][0], $ip);
                // 匹配端口 
                preg_match('/<td[^>]+>(.*?)<\/td>/', $td[0][1], $port);

                // 组装数据,写入
                $str = $ip[1] . ':' . $port[1];

                file_put_contents('./2.txt', $str . '@@@@', FILE_APPEND);
            }
        }

