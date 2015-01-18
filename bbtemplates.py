import re, json, random

NEWLINE = '<br>'
IMG = '<img src="{url}" alt="Image">'
B_START = '<span style="font-weight: bold">'
B_END = '</span>'
I_START = '<span style="font-style: italic">'
I_END = '</span>'
U_START = '<span style="text-decoration: underline">'
U_END = '</span>'
FONT_SIZE_START = '<span style="font-size: {n}%; line-height: 116%;">'
FONT_SIZE_END = '</span>'
FONT_COLOR_START = '<span style="color: {color_def}">'
FONT_COLOR_END = '</span>'
QUOTE_START = '<blockquote><div><cite>{user}</cite>'
QUOTE_END = '</div></blockquote>'
CODE = '<dl class="codebox"><dt>Code:<a href="#">Select all</a></dt><dd><code>{code}</code></dd></dl>'
LIST_START = '<ul>'
LIST_END = '</ul>'
ITEM_START = '<li>'
ITEM_END = '</li>'
URL_EXPLICIT = '<a href="{url}" class="postlink" target="_blank">{url_display}</a>'
URL_IMPLIED = '<a href="{url}" class="postlink" target="_blank">{url}</a>'
MLB = '<iframe src="http://mlb.mlb.com/shared/video/embed/embed.html?content_id={mlb_id}&amp;width=400&amp;height=224&amp;property=mlb" width="400" height="224" frameborder="0">Your browser does not support iframes.</iframe>'
VIMEO = '<iframe src="http://player.vimeo.com/video/{vimeo_id}?title=0&amp;byline=0&amp;portrait=0" width="400" height="225" frameborder="0" webkitallowfullscreen="" mozallowfullscreen="" allowfullscreen=""></iframe>'
YOUTUBE = '<object width="425" height="344"><param name="movie" value="https://www.youtube.com/v/{youtube_id}&amp;rel=en&amp;fs=1&amp;color1=0x234900&amp;color2=0xd4d4d4"><param name="allowFullScreen" value="true"><param name="allowscriptaccess" value="always"><embed src="https://www.youtube.com/v/1hYDYrdiYX8&amp;rel=en&amp;fs=1&amp;color1=0x234900&amp;color2=0xd4d4d4" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="425" height="344"></object>'

newline_patt = re.compile(r'\n')
img_patt = re.compile(r'\[img(?P<id>:\w+)?\](?P<url>.*)\[/img(?P=id)?\]')
b_start_patt = re.compile(r'\[b(?P<id>:\w+)?\]')
b_end_patt = re.compile(r'\[/b(?P<id>:\w+)?\]')
i_start_patt = re.compile(r'\[i(?P<id>:\w+)?\]')
i_end_patt = re.compile(r'\[/i(?P<id>:\w+)?\]')
u_start_patt = re.compile(r'\[u(?P<id>:\w+)?\]')
u_end_patt = re.compile(r'\[/u(?P<id>:\w+)?\]')
font_size_start_patt = re.compile(r'\[size=(?P<n>\d+)(?P<id>:\w+)?\]')
font_size_end_patt = re.compile(r'\[/size(?P<id>:\w+)?\]')
font_color_start_patt = re.compile(r'\[color=(?P<color_def>#?\w+)(?P<id>:\w+)?\]')
font_color_end_patt = re.compile(r'\[/color(?P<id>:\w+)?\]')
quote_start_patt = re.compile(r'\[quote(?:="(?P<user>.*)")?(?P<id>:\w+)?\]')
quote_end_patt = re.compile(r'\[/quote(?P<id>:\w+)?\]')
code_patt = re.compile(r'\[code(?P<id>:\w+)?\](?P<code>.*)\[/code(?P=id)?\]')
list_start_patt = re.compile(r'\[list(?P<id>:\w+)?\]')
list_end_patt = re.compile(r'\[/list(?P<id>:\w+)?\]')
item_start_patt = re.compile(r'\[\*(?P<id>:\w+)?\]')
item_end_patt = re.compile(r'\[/\*(?P<id>:\w+)?\]')
url_patt_explicit = re.compile(r'\[url=(?P<url>.*)(?P<id>:\w+)?\](?P<url_display>.*)\[/url(?P=id)?\]')
url_patt_implied = re.compile(r'\[url(?P<id>:\w+)?\](?P<url>.*)\[/url(?P=id)?\]')
mlb_patt = re.compile(r'\[videomlb(?P<id>:\w+)?\](?P<mlb_id>.+)\[videomlb(?P=id)?\]')
vimeo_patt = re.compile(r'\[vimeo(?P<id>:\w+)?\].*vimeo.com/(?P<vimeo_id>.+)\[/vimeo(?P=id)?\]')
youtube_patt = re.compile(r'\[youtube(?P<id>:\w+)?\].*youtube.com/watch\?v=(?P<youtube_id>[^&]+).*\[/youtube(?P=id)?\]')
#pattern_templates = [(newline_patt, NEWLINE),(img_patt, IMG), (b_start_patt, B_START), (b_end_patt, B_END), (i_start_patt, I_START), (i_end_patt, I_END), (u_start_patt, U_START), (u_end_patt, U_END), (font_size_start_patt, FONT_SIZE_START), (font_size_end_patt, FONT_SIZE_END), (font_color_start_patt, FONT_COLOR_START), (font_color_end_patt, FONT_COLOR_END), (quote_start_patt, QUOTE_START), (quote_end_patt, QUOTE_END), (code_patt, CODE), (list_start_patt, LIST_START), (list_end_patt, LIST_END), (item_start_patt, ITEM_START), (item_end_patt, ITEM_END), (url_patt_explicit, URL_EXPLICIT), (url_patt_implied, URL_IMPLIED), (mlb_patt, MLB), (vimeo_patt, VIMEO), (youtube_patt, YOUTUBE)]
pattern_templates = [(newline_patt, NEWLINE),(img_patt, IMG), (b_start_patt, B_START), (b_end_patt, B_END), (i_start_patt, I_START), (i_end_patt, I_END), (u_start_patt, U_START), (u_end_patt, U_END), (font_size_start_patt, FONT_SIZE_START), (font_size_end_patt, FONT_SIZE_END), (font_color_start_patt, FONT_COLOR_START), (font_color_end_patt, FONT_COLOR_END), (code_patt, CODE), (list_start_patt, LIST_START), (list_end_patt, LIST_END), (item_start_patt, ITEM_START), (item_end_patt, ITEM_END), (url_patt_explicit, URL_EXPLICIT), (url_patt_implied, URL_IMPLIED), (mlb_patt, MLB), (vimeo_patt, VIMEO), (youtube_patt, YOUTUBE)]

def replace_tags(post):
    for pattern, template in pattern_templates:
        scanner = pattern.scanner(post)
        m = scanner.search()
        while(m):
            post = post.replace(m.group(),template.format(**m.groupdict('')),1)
            m = scanner.search()
    return post

def replace_smilies_path(post):
    return post.replace('{SMILIES_PATH}','http://forums.hipinion.com/images/smilies')

def wrap_post(post):
    return '<div class="post bg1 unreadpost"><div class="inner"><span class="corners-top"></span><div class="postbody"><div class="content">{post}</div></div><span class="corners-bottom"></span></div></div>\n'.format(post=post)

if __name__ == '__main__':
    users = json.loads(open('data.1.json').read())
    with open('posts.html','w') as posthtml:
        posthtml.write('<html>')
        posthtml.write(open('bbheader').read())
        posthtml.write('<body><div id="wrap"><div id="page-body">')
        for user in users['users']:
            for post in user['posts']:
                if post and random.random() < .001:
                    posthtml.write(wrap_post(replace_smilies_path(replace_tags(post))))
        posthtml.write('</div></div></body></html>')
