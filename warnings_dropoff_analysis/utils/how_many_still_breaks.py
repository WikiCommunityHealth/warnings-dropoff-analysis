# -*- coding: utf-8 -*-

import gzip
import json

# retired template keywords list
retired_template_list = [
    'visszavonult', 
    'lämnat', 
    '永遠離開', 
    'utilizator retras', 
    'کاربر بازنشسته', 
    'vertrokken', 
    'অবসরপ্রাপ্ত', 
    'retraité', 
    'pasitraukęs', 
    'պաշտոնաթող', 
    'විශ් රාමික', 
    'повлечен корисник', 
    'سبک دوش', 
    'emekli', 
    'deaktiviert', 
    'pènsiyun', 
    'పూర్తి విరమణ', 
    'usuário inativo', 
    'qeyri-aktiv', 
    'சுயவிடுப்பு', 
    'đã nghỉ việc', 
    'متقاعد', 'retired', 
    'usuario retirado', 
    'utente ritirato', 
    'เกษียณ', 'neaktiven', 
    'retirado', 
    '위키백과탈퇴', 
    'خانەنشین', 
    'jo aktiv', 
    'неактивен потребител'
]

retired_counter = 0

if __name__ == '__main__':
    print('Analyzing how many users are in retirement')
    with gzip.open('wiki_breaks/eswiki.json.gz') as f:
        for line in f:
            obj = json.loads(line)
            for wb in obj['wikibreaks']:
                if wb['name'] in retired_template_list and not wb['to_date']:
                    retired_counter += 1
    print('Found {}'.format(retired_counter))
