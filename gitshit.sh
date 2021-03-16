#!/bin/bash
git add -A
echo "comentario :"
read comentario
git commit -m "$comentario"
echo "push!!!"
git push
