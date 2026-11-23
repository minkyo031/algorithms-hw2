"""Small, standard-library URL shortening service."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit
from html import escape
from .shortener import URLShortener
from .hash_table import horner, horner_steps, HashTable

shorteners = [URLShortener('chaining', 17), URLShortener('linear', 17)]

def page(body):
    return ('<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>URL Shortener</title><style>body{font:16px system-ui;max-width:980px;margin:35px auto;padding:0 18px;color:#203044}'
            'input{width:65%;padding:12px}button,select{padding:12px}a{color:#155e9b}pre{white-space:pre-wrap;word-break:break-all}'
            '.slot{border:1px solid #d7deea;border-radius:8px;margin:8px 0;padding:12px}details{margin:8px 0}'
            '.node{background:#eaf3fa;padding:8px;border-radius:4px;display:inline-block;max-width:95%;overflow-wrap:anywhere}'
            '</style><h1>URL 단축기</h1><nav><a href="/">홈</a> · <a href="/table">테이블 보기</a></nav>' + body + '</html>')

class Handler(BaseHTTPRequestHandler):
    def respond(self, content, status=200, headers=None):
        data = content.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type','text/html; charset=utf-8')
        self.send_header('Content-Length',str(len(data)))
        self.send_header('Cache-Control','no-store')
        if headers:
            for k,v in headers: self.send_header(k,v)
        self.end_headers()
        self.wfile.write(data)

    def root(self, result=''):
        self.respond(page('<p>http 또는 https 주소를 입력하세요.</p><form method="post" action="/shorten">'
            '<input type="url" name="url" required placeholder="https://example.com/path">'
            '<select name="mode"><option value="chaining">개별 체이닝</option><option value="linear">선형 탐지</option></select>'
            '<button type="submit">줄이기</button></form>' + result))

    def base_url(self):
        host = self.headers.get('X-Forwarded-Host') or self.headers.get('Host', 'localhost:8000')
        proto = self.headers.get('X-Forwarded-Proto') or 'http'
        if proto not in ('https','http'): proto = 'http'
        if '\n' in host or '\r' in host: host='localhost:8000'
        return proto+'://'+host

    def do_POST(self):
        if urlsplit(self.path).path != '/shorten': return self.respond(page('없는 페이지'), 404)
        try:
            length = int(self.headers.get('Content-Length','0'))
            if length > 10000: return self.respond(page('요청이 너무 큽니다'),413)
            fields = parse_qs(self.rfile.read(length).decode('utf-8'))
            mode = fields.get('mode',['chaining'])[0]
            if mode not in ('chaining','linear'): raise ValueError('알 수 없는 테이블 방식')
            code = shorteners[0 if mode == 'chaining' else 1].shorten(fields.get('url',[''])[0])
            link = self.base_url()+'/'+mode+'/'+code
            self.root('<p>단축 주소: <a href="'+escape(link,quote=True)+'">'+escape(link)+'</a></p>')
        except (ValueError,UnicodeError) as exc:
            self.root('<p style="color:crimson">입력 오류: '+escape(str(exc))+'</p>')

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == '/': return self.root()
        if path == '/table': return self.table_page()
        parts = path.strip('/').split('/')
        if len(parts)==2 and parts[0] in ('chaining','linear'):
            s = shorteners[0 if parts[0]=='chaining' else 1]
            url = s.resolve(parts[1])
            if url is None: return self.respond(page('코드를 찾을 수 없습니다'),404)
            self.send_response(302)
            self.send_header('Location',url)
            self.send_header('Content-Length','0')
            self.end_headers()
            return
        return self.respond(page('없는 페이지'),404)

    def table_page(self):
        body = '<p>두 테이블의 URL → 코드 데이터 저장 상태와 호너 해시 계산입니다.</p>'
        for s in shorteners:
            table = s.url_to_code
            body += '<h2>'+('개별 체이닝' if s.table_type=='chaining' else '선형 탐지')+' · M='+str(table.capacity)+'</h2>'
            for i in range(table.capacity):
                if isinstance(table, HashTable):
                    items=[]; cur=table.buckets[i]
                    while cur:
                        items.append((cur.key,cur.value));cur=cur.next
                else:
                    items=[] if table.slots[i] is None else [table.slots[i]]
                body += '<div class="slot"><strong>['+str(i)+']</strong> '
                if not items: body += '∅'
                for key,code in items:
                    initial=horner(key,table.capacity)
                    origin=' (원래 해시 '+str(initial)+', 탐지 '+str((i-initial)%table.capacity)+'칸)' if s.table_type=='linear' else ''
                    steps='\n'.join('h = (31 × '+str(old)+' + '+str(n)+') % '+str(table.capacity)+' = '+str(new)+'  '+ch for ch,old,n,new in horner_steps(key,table.capacity))
                    link=self.base_url()+'/'+s.table_type+'/'+code
                    body += '<span class="node">'+escape(key)+' → '+escape(code)+' → <a href="'+escape(link,quote=True)+'">'+escape(link)+'</a>'+origin+'</span> → '
                    body += '<details><summary>호너 해시 계산 보기</summary><pre>'+escape(steps)+'</pre></details>'
                body += 'NULL</div>' if s.table_type=='chaining' else '</div>'
        self.respond(page(body))

def main():
    server = ThreadingHTTPServer(('0.0.0.0',8000),Handler)
    print('Listening on http://localhost:8000',flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()

if __name__=='__main__': main()
