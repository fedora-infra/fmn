import md5 from 'crypto-js/md5'

export function generateLibravatarURL(email: string, size = 80, defaulticon = "retro"): string {
    let hash = md5(email);
    return "https://www.libravatar.org/avatar/"+hash+"?s="+size.toString()+"&d="+defaulticon;
  }
