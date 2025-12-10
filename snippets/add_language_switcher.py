#!/usr/bin/env python3
"""
批量為所有 MDX 文件添加語言切換器
"""

import os
import re

# 語言配置
LANGUAGES = {
    'en': {'flag': '🇺🇸', 'label': 'English'},
    'zh': {'flag': '🇹🇼', 'label': '繁體中文'},
    'zh-CN': {'flag': '🇨🇳', 'label': '简体中文'},
    'ja': {'flag': '🇯🇵', 'label': '日本語'},
    'ko': {'flag': '🇰🇷', 'label': '한국어'}
}

def generate_language_switcher(current_lang, page_path):
    """生成語言切換器的 HTML"""
    lines = [
        "<div style={{padding: '1rem', backgroundColor: '#f8f9fa', borderRadius: '8px', marginBottom: '2rem', border: '1px solid #e9ecef'}}>",
        "  <div style={{fontSize: '0.875rem', fontWeight: '600', marginBottom: '0.5rem', color: '#495057'}}>🌐 Language / 語言</div>",
        "  <div style={{display: 'flex', gap: '0.5rem', flexWrap: 'wrap'}}>"
    ]
    
    for lang_code, lang_info in LANGUAGES.items():
        is_current = (lang_code == current_lang)
        style_props = {
            'padding': '0.5rem 1rem',
            'borderRadius': '6px',
            'textDecoration': 'none',
            'fontSize': '0.875rem',
        }
        
        if is_current:
            style_props.update({
                'fontWeight': '600',
                'backgroundColor': '#0ABAB5',
                'color': '#ffffff',
                'border': '1px solid #0ABAB5'
            })
        else:
            style_props.update({
                'backgroundColor': '#ffffff',
                'color': '#495057',
                'border': '1px solid #dee2e6'
            })
        
        style_str = ', '.join([f"{k}: '{v}'" for k, v in style_props.items()])
        href = f"/{lang_code}/{page_path}"
        label = f"{lang_info['flag']} {lang_info['label']}"
        
        # 使用字符串格式化避免 f-string 的花括號問題
        line = f"    <a href=\"{href}\" style={{{{{style_str}}}}}}}>{label}</a>"
        lines.append(line)
    
    lines.extend([
        "  </div>",
        "</div>",
        ""
    ])
    
    return '\n'.join(lines)

def process_mdx_file(filepath, lang_code):
    """處理單個 MDX 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 檢查是否已有語言切換器
    if '🌐 Language' in content:
        print(f"  已有語言切換器，跳過: {filepath}")
        return False
    
    # 找到 frontmatter 結束位置
    parts = content.split('---\n', 2)
    if len(parts) < 3:
        print(f"  無法找到frontmatter: {filepath}")
        return False
    
    frontmatter = parts[1]
    body = parts[2]
    
    # 從filepath提取頁面路徑
    # 例如: en/aboutmilwaysfinancecard.mdx -> aboutmilwaysfinancecard
    page_path = os.path.splitext(os.path.basename(filepath))[0]
    
    # 生成語言切換器
    switcher = generate_language_switcher(lang_code, page_path)
    
    # 組合新內容
    new_content = f"---\n{frontmatter}---\n\n{switcher}\n{body}"
    
    # 寫回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✓ 已添加語言切換器: {filepath}")
    return True

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)
    
    # 處理所有頁面：主要頁面 + essentials 目錄中的頁面
    pages_config = [
        # 根目錄頁面
        {'file': 'aboutmilwaysfinancecard.mdx', 'path': ''},
        {'file': 'accountsetup.mdx', 'path': ''},
        # essentials 目錄頁面
        {'file': 'set2fa.mdx', 'path': 'essentials/'},
        {'file': 'setpin.mdx', 'path': 'essentials/'},
        {'file': 'deposittowallet.mdx', 'path': 'essentials/'},
        {'file': 'topupcreditcard.mdx', 'path': 'essentials/'},
        {'file': 'addtogooglewallet.mdx', 'path': 'essentials/'},
        {'file': 'wallettransfer.mdx', 'path': 'essentials/'},
        {'file': 'sendreferralurl.mdx', 'path': 'essentials/'},
        {'file': 'resetting-password.mdx', 'path': 'essentials/'},
        {'file': 'applyphysicalcard.mdx', 'path': 'essentials/'},
        {'file': 'applycardwithactivationcode.mdx', 'path': 'essentials/'},
        {'file': 'addtohomescreen.mdx', 'path': 'essentials/'},
    ]
    
    total_processed = 0
    total_skipped = 0
    
    for lang_code in LANGUAGES.keys():
        lang_dir = os.path.join(project_root, lang_code)
        if not os.path.exists(lang_dir):
            print(f"語言目錄不存在: {lang_dir}")
            continue
        
        print(f"\n處理 {lang_code}/...")
        
        for page_config in pages_config:
            page_file = page_config['file']
            page_path = page_config['path']
            
            # 完整文件路徑
            if page_path:
                filepath = os.path.join(lang_dir, page_path, page_file)
            else:
                filepath = os.path.join(lang_dir, page_file)
            
            if os.path.exists(filepath):
                # 從文件路徑提取頁面路徑（用於生成URL）
                page_url_path = page_path + os.path.splitext(page_file)[0]
                
                # 修改 process_mdx_file 函數調用
                result = process_mdx_file_with_path(filepath, lang_code, page_url_path)
                if result:
                    total_processed += 1
                else:
                    total_skipped += 1
            else:
                print(f"  文件不存在: {filepath}")
    
    print(f"\n\n總計：")
    print(f"  ✓ 已處理: {total_processed} 個文件")
    print(f"  - 已跳過: {total_skipped} 個文件（已有語言切換器）")

def process_mdx_file_with_path(filepath, lang_code, page_url_path):
    """處理單個 MDX 文件（支持自定義頁面路徑）"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 檢查是否已有語言切換器
    if '🌐 Language' in content:
        print(f"  已有語言切換器，跳過: {filepath}")
        return False
    
    # 找到 frontmatter 結束位置
    parts = content.split('---\n', 2)
    if len(parts) < 3:
        print(f"  無法找到frontmatter: {filepath}")
        return False
    
    frontmatter = parts[1]
    body = parts[2]
    
    # 生成語言切換器
    switcher = generate_language_switcher(lang_code, page_url_path)
    
    # 組合新內容
    new_content = f"---\n{frontmatter}---\n\n{switcher}\n{body}"
    
    # 寫回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✓ 已添加語言切換器: {filepath}")
    return True

if __name__ == '__main__':
    main()

