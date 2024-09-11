#!/bin/bash


PARAMS=""
original_parameters="$@"
#Source: https://medium.com/@Drew_Stokes/bash-argument-parsing-54f3b81a6a8f
while (( "$#" )); do
    case "$1" in
        --reinit|-ri)
            reinit=1
            shift 1
            ;;
        --root)
            root=1
            shift 1
            ;;
        --user)
            user=$2
            shift 2
            ;;
        --) # end argument parsing
            shift
            break
            ;;
        -help|--help)
            echo "docky [image]"
            echo ""
            echo " A helper tool that manages basic enviroments and long live containers for working folders"
            echo ""
            echo "  -reinit "
            echo "      Initialize again the docker image, this will drop every change that you have done compared to the image"
            echo "      and create an clean container from the image."
            exit 0
            ;;
        -*|--*=) # unsupported flags
            echo "Error: Unsupported flag $1" >&2
            exit 99
            ;;
        *) # preserve positional arguments
            PARAMS="$PARAMS $1"
            shift
            ;;
    esac
done
eval set -- "$PARAMS"

if [ -z $1 ]; then
    echo "We need an image to be set in the positional argument or docky file"
    exit
fi

imageName="$1"
imageId="docky-$1"
mainFolder="$PWD"

containerNameSpecPart="`readlink -f $mainFolder | tr "/" "_"| cut -c2- | iconv -f utf8 -t ascii//TRANSLIT | sed -e 's/[^a-zA-Z0-9_.-]//g'`"
containerName="docky_${containerNameSpecPart}_$imageName"
echo "Container name: $containerName" 



hostname="$containerNameSpecPart"
echo "Hostname: $hostname"



if [ ! -z $reinit ]; then
    echo "reinit activated"
    if docker container ls --format "{{.Names}}" |grep -E "^$containerName$"; then
        echo "Stopping running container"
        docker stop $containerName
    fi
    if docker container ls --all --format "{{.Names}}" |grep -E "$containerName"; then
        echo "Removing existing container"        
        docker rm $containerName    
    fi
    echo "Clean done for reiniting"
fi


extraParams=()
   

if [ ! -z $root ]; then
    extraParams+=("-u" "root")
fi

if [ ! -z $user ]; then
    extraParams+=("-u" "$user")
fi

echo $imageId

if docker container ls --format "{{.Names}}" |grep -E "^$containerName$"; then
    echo "Container already running, attaching new session"
    docker exec -it "${extraParams[@]}" $containerName bash
elif docker container ls --all --format "{{.Names}}" |grep -E "^$containerName$"; then
    echo "Container already exist, starting it"
    docker container start $containerName &&
    docker exec -it "${extraParams[@]}" $containerName bash
else
    echo "Container not running, initiating"
    docker run --name $containerName "${extraParams[@]}" --hostname $hostname -p 81:80  -it -v "$PWD:/home/docky/app" -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix $imageId 
fi






