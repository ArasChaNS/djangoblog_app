from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,reverse
from .forms import ArticleForm
from django.contrib import messages
from .models import Article,Comment
from django.contrib.auth.decorators import login_required
# Create your views here.

def articles(request):
    keyword = request.GET.get("keyword")

    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request,"articles.html",{"articles": articles})
    articles = Article.objects.all()



    articles = Article.objects.all()

    return render(request,"articles.html",{"articles" : articles})

def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")
def dashboard(request):
    if not request.user.is_authenticated:
        messages.info(request, "Bu Sayfayı Görmek İçin Giriş Yapın...")
        return render(request,"login.html")

    articles = Article.objects.filter(author = request.user)

    context = {
        "articles" : articles
    }
    return render(request,"dashboard.html",context)


def addarticle(request):
    if not request.user.is_authenticated:
        messages.info(request, "Bu Sayfayı Görmek İçin Giriş Yapın...")
        return render(request,"index.html")



    form = ArticleForm(request.POST or None,request.FILES or None)

    if form.is_valid():
        
        article = form.save(commit=False)

        article.author = request.user
        article.save()
        messages.success(request,"Makale Başarıyla Oluşturuldu")
        return redirect("index")


    return render(request,"addarticle.html",{"form" : form})


def detail(request,id):
    #article = Article.objects.filter(id = id).first()   
    article = get_object_or_404(Article, id=id)
    comments = article.comments.all()
    return render(request,"detail.html",{"article":article,"comments":comments })

    


def updateArticle(request,id):
    
    article = get_object_or_404(Article,id = id)
    form = ArticleForm(request.POST or None,instance = article)
    if form.is_valid():
        article = form.save(commit=False)

        article.author = request.user
        article.save()
        messages.success(request,"Makale Başarıyla Güncellendi")
        return redirect("index")


    
    return render(request,"update.html",{"form" : form})

def deleteArticle(request,id):
    article = get_object_or_404(Article,id = id)
    article.delete()

    messages.success(request,"Makale Başarıyla Silindi")
    return render(request,"index.html")


def addComment(request,id):
    article = get_object_or_404(Article, id=id)

    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author  = comment_author, comment_content = comment_content)

        newComment.article = article

        newComment.save()
    return redirect(reverse("article:detail",kwargs={"id":id}))