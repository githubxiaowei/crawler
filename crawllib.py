

def save_text(response,file):
    with open(file,'w',encoding='utf8') as f:
        f.write(str(response.content,'utf8'))
        
      