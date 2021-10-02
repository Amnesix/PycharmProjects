#!/usr/bin/env sh
resultat=0

question() {
  python3 -m MsgBox -t "Quizz" -m "$1" --b $2 --icon question --timeout 20
  res=$?
  if [ $res -eq $3 ]
  then
    return 1
  fi
  return 0
}
question "Calculate 5×15" "55;75;85;105" 1
res=$?
resultat=$(($resultat+$res))
question "Calculate 3×18" "36;46;48;52;54;58" 4
res=$?
resultat=$(($resultat+$res))
question "Calculate 4×16" "48;64;80;96" 1
res=$?
resultat=$(($resultat+$res))
echo $resultat / 3