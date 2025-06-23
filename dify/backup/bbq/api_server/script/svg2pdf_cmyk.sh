#!/bin/bash
# svg2cmyk.sh - 将SVG批量转换为CMYK矢量PDF

# 1. 检查依赖
if ! command -v inkscape &> /dev/null; then
  echo "错误：未安装Inkscape，请执行 'apt install inkscape' 或 'brew install inkscape'"
  exit 1
fi

if ! command -v gs &> /dev/null; then
  echo "错误：未安装Ghostscript，请执行 'apt install ghostscript' 或 'brew install ghostscript'"
  exit 1
fi

# 2. 定义配置文件路径（需提前下载）
CMYK_PROFILE="/home/qinbinbin/ai_tools/comfyui/tmp/ISOcoated_v2_300_eci.icc"

# 3. 处理单个文件
convert_file() {
  local svg_file=$1
  local pdf_temp=$(basename "$svg_file" .svg)_temp.pdf
  local pdf_cmyk=$(basename "$svg_file" .svg)_CMYK.pdf

  # 导出SVG到PDF（使用新的参数格式）
  inkscape "$svg_file" --export-type=pdf --export-filename="$pdf_temp"

  # 转换PDF到CMYK
  # 检查配置文件是否存在
  if [ -f "$CMYK_PROFILE" ]; then
    gs -sDEVICE=pdfwrite \
       -dProcessColorModel=/DeviceCMYK \
       -sOutputFile="$pdf_cmyk" \
       -sDefaultCMYKProfile="$CMYK_PROFILE" \
       -dPreserveOverprintSettings=true \
       -dNOPAUSE \
       -dBATCH \
       -dSAFER \
       "$pdf_temp"
  else
    echo "警告：未找到ICC配置文件，使用默认CMYK设置"
    gs -sDEVICE=pdfwrite \
       -dProcessColorModel=/DeviceCMYK \
       -sOutputFile="$pdf_cmyk" \
       -dPreserveOverprintSettings=true \
       -dNOPAUSE \
       -dBATCH \
       -dSAFER \
       "$pdf_temp"
  fi

  # 清理临时文件
  if [ -f "$pdf_temp" ]; then
    rm "$pdf_temp"
  fi
  echo "已完成转换：$pdf_cmyk"
}

# 4. 批量处理
if [ -d "$1" ]; then
  # 处理目录下所有SVG文件
  for svg in "$1"/*.svg; do
    convert_file "$svg"
  done
elif [ -f "$1" ]; then
  # 处理单个文件
  convert_file "$1"
else
  echo "用法：$0 <SVG文件或目录>"
  exit 1
fi
