class ContentLoader{
	constructor(){
		console.log("loading content start");
		var actionLoader:ConfigLoader = new ConfigLoader(ELoad.services, "../config/poskytovane_sluzby.json");
		var announcmentLoader:ConfigLoader = new ConfigLoader(ELoad.announcement, "../config/oznameni.json");
	}
}

enum ELoad{
	services,
	announcement
}

class ConfigLoader{
	private _request:XMLHttpRequest;
	
	constructor(private _type:ELoad, url:string){
		this._request = new XMLHttpRequest();
		this._request.addEventListener("readystatechange", this.responseHandler.bind(this));
		this._request.open("POST", url, true);
		this._request.send();
	}
	
	private responseHandler():void {
		if(this._request.readyState == 4 && this._request.status == 200){
			// console.log("response: "+this._request.responseText);
			if(this._type == ELoad.services){
				this.createActionItems(this._request.responseText);
			}else{
				this.createAnnouncementItems(this._request.responseText);
			}
		}
	}
	
	private createActionItems(data:string):void{
		var items:Array<ActionItem> = [];
		var services:Array<Object> = JSON.parse(data).services;
		services.forEach(action => {
			var actionItem:ActionItem = new ActionItem(action["oblast"],action["sluzby"]);
			items.push(actionItem);
		});
		this.addItem(items);
	}
	
	private createAnnouncementItems(data:string):void{
		var items:Array<AnnouncementItem> = [];
		var announcements:Array<Object> = JSON.parse(data).oznameni;
		if (announcements.length && announcements.length > 0) {
			announcements.forEach(announcement => {
				var announcementItem:AnnouncementItem = new AnnouncementItem(announcement["datum"],announcement["text"]);
				items.push(announcementItem);
			});
		} else {
			console.log("add mock")
			var date:Date = new Date();
			var nodataItem:AnnouncementItem = new AnnouncementItem(date.getDate()+"."+(date.getMonth()+1)+"."+date.getFullYear(), "Žádná oznámení.");
			items.push(nodataItem);
		}
		this.addItem(items);
	}
	
	private addItem(items:Array<any>){
		var itemsContainer:HTMLElement;
		if (this._type == ELoad.services) {
			itemsContainer = document.getElementById("services"); 
		} else {
			itemsContainer = document.getElementById("aItemContainer");
		}
		items.forEach(item => {
			//TODO efetk pridani
			itemsContainer.appendChild(item.item);
		});
	}
}

class ActionItem {
	public item:HTMLElement;
	constructor(title:string, actions:Array<string>){
		this.item = document.createElement("div");
		
		var heading:HTMLHeadingElement = <HTMLHeadingElement>document.createElement("h4");
		heading.innerHTML = title;
		this.item.appendChild(heading);
		
		var actionList:HTMLUListElement = <HTMLUListElement>document.createElement("ul");
		this.item.appendChild(actionList);
		
		actions.forEach(action => {
			var actionElement:HTMLLIElement = <HTMLLIElement>document.createElement("li");
			actionElement.innerHTML = action;
			actionList.appendChild(actionElement);
		});
	}
}

class AnnouncementItem{
	public item:HTMLElement;
	constructor(date:string, text:string){
		this.item = document.createElement("div");
		this.item.style.cssText = "width:100%;margig-bottom:10px;";
		
		var dateElement:HTMLElement = document.createElement("div");
		dateElement.style.paddingRight = "5px";
		dateElement.innerHTML = date + " :";
		this.item.appendChild(dateElement);
		
		var textElement:HTMLElement = document.createElement("div");
		textElement.innerHTML = text;
		this.item.appendChild(textElement);
	}
}