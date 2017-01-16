" ------------------------------------------------------------------------------
" Plugin: Generate JSDoc Function Documention
" Author: Aaron Cepukas
" ------------------------------------------------------------------------------

let s:JSDocVimScriptPath = expand('<sfile>:p:h')

function! s:JSDocGetFn()
  let l:originalPosition = getpos('.')
  let l:startLine = l:originalPosition[1]
  call search('{', 'e')
  let l:endLine = searchpair('{', '', '}')
  let l:lines = getline(l:startLine, l:endLine)
  call setpos('.', l:originalPosition)
  return join(l:lines, '')
endfunction

function! s:JSDocSnipFn()
  if executable('python2')
    let l:scriptPath = s:JSDocVimScriptPath . '/gen-jsdoc-fn.py'
    return system('python2 ' . l:scriptPath, shellescape(s:JSDocGetFn()))
  else
    echom "python2 is not available on your system"
  endif
endfunction

if exists('g:generateJSDocFuncDocKeyMap') && exists('*UltiSnips#Anon')
  let s:cmd = [
    \"inoremap <silent>",
    \g:generateJSDocFuncDocKeyMap,
    \"<C-R>=UltiSnips#Anon(<SID>JSDocSnipFn(), '', '', 'i')<cr>"
    \]
  execute join(s:cmd, ' ')
endif
