## async-load
# *A tool for asynchronously loading other scripts which has been adapted
# from http://css-tricks.com/thinking-async/*

oldElement = document.getElementsByTagName('script')[0]

insert = (tagName, url, id) ->
  if document.getElementById id then return

  newElement = document.createElement tagName
  newElement.src = url
  id && newElement.id = id
  oldElement.parentNode.insertBefore newElement, oldElement

# Local library.
